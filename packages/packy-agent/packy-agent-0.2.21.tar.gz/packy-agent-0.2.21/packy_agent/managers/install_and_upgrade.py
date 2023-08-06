import logging
import os
import os.path
import shutil

from jinja2 import Template
from pkg_resources import parse_version

import packy_agent
from packy_agent.utils.pkg_resources import get_package_file_content, get_package_file_full_path
from packy_agent.configuration.control_server.base import configuration
from packy_agent.configuration.agent.base import configuration as packy_agent_configuration
from packy_agent.managers.control import (control_manager,
    AGENT_SUPERVISOR_NAME, CONTROL_SERVER_SUPERVISOR_NAME, WATCHDOG_SUPERVISOR_NAME)
from packy_agent.utils.shell import install_ubuntu_packages, install_alpine_packages, run_command
from packy_agent.utils.network import get_machine_ip_address, get_hostname_from_url
from packy_agent.utils.services.systemd import packy_service, nginx_service, log2ram_service
from packy_agent.utils.output import write_to_console_or_file
from packy_agent.utils.misc import (
    run_shell_command_async, get_executable_path, is_inside_docker_container)
from packy_agent.clients.packy_server import PackyServerClient
from packy_agent.exceptions import AuthenticationError, ValidationError
from packy_agent.utils.auth import is_activated
from packy_agent.clients.packy_server import packy_server_client_factory


logger = logging.getLogger(__name__)

UBUNTU_CONFIGURE_TARGET = 'ubuntu'
DOCKER_CONFIGURE_TARGET = 'docker'
CONFIGURE_TARGETS = (UBUNTU_CONFIGURE_TARGET, DOCKER_CONFIGURE_TARGET)


def get_pip_command_args(version=None, extra_options=None, package_def='packy-agent'):
    package = '{}=={}'.format(package_def, version) if version else package_def
    return ['install'] + (extra_options or []) + [
        '--extra-index-url', configuration.get_packy_agent_pypi_repository(), package]


def get_pip_upgrade_packy_package_args(version=None, package_def='packy-agent'):
    return get_pip_command_args(version=version,
                                extra_options=['--upgrade', '--no-deps', '--force-reinstall'],
                                package_def=package_def)


def get_pip_install_dependencies_args(version=None, package_def='packy-agent'):
    return get_pip_command_args(version=version, package_def=package_def)


def args_to_pip_command(args):
    return get_executable_path('pip') + ' ' + ' '.join(args)


def render_template_from_package_file_content(template_module_name, template_filename,
                                              context=None):
    template_text = get_package_file_content(template_module_name, template_filename)
    template = Template(template_text)
    return template.render(**(context or {}))


class InstallAndUpgradeManager(object):

    def activate(self, email, password, async_restart=True):
        if is_activated():
            raise ValidationError('Agent has already been activated')

        client = PackyServerClient(configuration.get_server_base_url())
        response = client.activate_agent(email, password)
        status_code = response.status_code
        if status_code == 401:
            raise AuthenticationError('Invalid credentials for agent activation')
        elif status_code == 400:
            payload = response.json()
            errors = payload.get('errors') or {}
            non_field_errors = errors.pop('non_field_errors', None) or []
            messages = ([payload.get('message')] + non_field_errors +
                        ['{}: {}.'.format(k, v) for k, v in errors.iteritems()])

            raise ValidationError(' '.join(filter(None, messages)))

        response.raise_for_status()

        agent_configuration = response.json()['configuration']
        packy_agent_configuration.save_local_configuration(agent_configuration)

        # TODO(dmu) LOW: Instead of always restart do according to current running status
        control_manager.restart_packy_agent(delay_seconds=1 if async_restart else None)

    def install_and_restart(self, version=None, delay_seconds=None):
        client = packy_server_client_factory.get_client_by_configuration(packy_agent_configuration)
        version_max = client.get_version_max()
        if version is None:
            version = version_max
        else:
            if version_max and parse_version(version) > parse_version(version_max):
                raise ValueError('Could not install/upgrade to version {} '
                                 '(it is higher than {})'.format(version, version_max))

        logger.info('Upgrading and restarting...')
        if not configuration.is_upgrade_enabled():
            logger.info('Upgrade was disabled (for developer protection)')

        python_executable = get_executable_path('python')
        command = ' && '.join((
            args_to_pip_command(get_pip_upgrade_packy_package_args(version=version)),
            args_to_pip_command(get_pip_install_dependencies_args(version=version)),
            # Running configure as a separate process to execute new version of code
            '{python_executable} -m packy_agent.cli.configure {target} {server_base_url}'.format(
                python_executable=python_executable,
                # TODO(dmu) MEDIUM: It is not safe to consider being under ubuntu if not in docker.
                #                   Refactor to have full feature OS recognition system
                target=(DOCKER_CONFIGURE_TARGET if is_inside_docker_container() else
                        UBUNTU_CONFIGURE_TARGET),
                server_base_url=configuration.get_server_base_url(),
            ),
        ))
        run_shell_command_async(command, delay_seconds=delay_seconds)

    def upgrade_and_restart(self, delay_seconds=None):
        self.install_and_restart(delay_seconds=delay_seconds)

    # TODO(dmu) MEDIUM: Refactor to use Ansible for most of these stuff
    def get_control_server_link(self, packy_server_base_url):
        # TODO(dmu) LOW: Unhardcode schema: `http://`
        link = 'http://' + get_machine_ip_address(get_hostname_from_url(packy_server_base_url))
        port = configuration.get_control_server_port()
        if port != 80:
            link += ':{}'.format(port)

        return link

    def configure_ubuntu(self, packy_server_base_url):
        install_ubuntu_packages(
            ('libssl-dev', 'libffi-dev', 'libsasl2-dev', 'liblz4-dev', 'libcurl4-openssl-dev',
             'nginx'), one_command=False)
        run_command(args_to_pip_command(get_pip_command_args(
            version=packy_agent.__version__,
            package_def='packy-agent[post]')))
        self.save_packy_server_base_url(packy_server_base_url)

        self.create_auxiliary_directories()
        self.generate_uwsgi_ini()
        self.generate_nginx_conf()
        self.generate_supervisord_configuration()
        self.setup_packy_service()

        nginx_service.restart(raise_exception=True)

    def configure_docker(self, packy_server_base_url, restart=True):
        install_alpine_packages(('curl-dev', 'nginx'), one_command=False)
        run_command(args_to_pip_command(get_pip_command_args(
            version=packy_agent.__version__,
            extra_options=['--global-option="--with-openssl"'],
            package_def='packy-agent[post]')))
        self.save_packy_server_base_url(packy_server_base_url)

        self.create_auxiliary_directories()
        self.generate_uwsgi_ini()

        nginx_log_dir = '/var/log/nginx'
        os.system('mkdir -p {}'.format(nginx_log_dir))
        os.system('chmod a+rwx {}'.format(nginx_log_dir))
        shutil.copy2(get_package_file_full_path('packy_agent.configuration',
                                                'templates/nginx_docker.conf'),
                     '/etc/nginx/nginx.conf')

        self.generate_nginx_conf(configuration_file='/etc/nginx/conf.d/packy-agent.conf')
        self.generate_supervisord_configuration()

        if restart:
            control_manager.restart(delay_seconds=5)

    def configure(self, target, packy_server_base_url, restart=True):
        if target == UBUNTU_CONFIGURE_TARGET:
            self.configure_ubuntu(packy_server_base_url)
        elif target == DOCKER_CONFIGURE_TARGET:
            self.configure_docker(packy_server_base_url, restart=restart)
        else:
            raise ValueError('Configuring for "{}" is not supported'.format(target))

    def setup_packy_service(self):
        logger.info('Setting up packy service')
        packy_service.update_initd_script(self.get_packy_initd_script_content('ubuntu'))
        packy_service.update_unit_service_configuration(self.get_packy_service_config_content())
        packy_service.stop()
        packy_service.start(raise_exception=True)

    def save_packy_server_base_url(self, packy_server_base_url):
        logger.info('Saving Packy Serve base URL: %s', packy_server_base_url)
        configuration.load_local_configuration()
        configuration.local_configuration.setdefault('packy', {}).setdefault(
            'control_server', {})['server_base_url'] = packy_server_base_url
        configuration.save_local_configuration()

    def get_packy_initd_script_content(self, operating_system):
        if operating_system == 'ubuntu':
            template_filename = 'templates/control-scripts/ubuntu/initd.sh'
        else:
            raise ValueError('Operating system "{}" is not supported'.format(operating_system))

        context = {
            'supervisord_executable': get_executable_path('supervisord'),
            'supervisorctl_executable': get_executable_path('supervisorctl'),
            'supervisor_log_directory': configuration.get_supervisor_log_directory(),
            'supervisor_run_directory': configuration.get_supervisor_run_directory(),
            'supervisor_configuration_file': configuration.get_supervisor_configuration_file(),
        }

        return render_template_from_package_file_content(
            'packy_agent.configuration', template_filename, context)

    def generate_packy_initd_script(self, operating_system, target_file):
        logger.info('Generating Packy initd script to %s', target_file)
        write_to_console_or_file(target_file, self.get_packy_initd_script_content(operating_system))

    def get_packy_service_config_content(self):
        context = {
            'supervisord_executable': get_executable_path('supervisord'),
            'supervisorctl_executable': get_executable_path('supervisorctl'),
            'supervisor_run_directory': configuration.get_supervisor_run_directory(),
            'supervisor_configuration_file': configuration.get_supervisor_configuration_file(),
        }

        return render_template_from_package_file_content(
            'packy_agent.configuration', 'templates/control-scripts/ubuntu/packy.service', context)

    def generate_supervisord_configuration(self, configuration_file=None):
        configuration_file = (configuration_file or
                              configuration.get_supervisor_configuration_file())
        logger.info('Generating Supervisor configuration file content to %s', configuration_file)

        context = {
            'supervisor_log_file': configuration.get_supervisor_log_file(),
            'supervisor_run_directory': configuration.get_supervisor_run_directory(),
            'control_server_stdout_log_file': configuration.get_control_server_stdout_log_file(),
            'control_server_stderr_log_file': configuration.get_control_server_stderr_log_file(),
            'agent_stdout_log_file': configuration.get_agent_stdout_log_file(),
            'agent_stderr_log_file': configuration.get_agent_stderr_log_file(),
            'watchdog_stdout_log_file': configuration.get_watchdog_stdout_log_file(),
            'watchdog_stderr_log_file': configuration.get_watchdog_stderr_log_file(),
            'venv_bin_dir': os.path.dirname(get_executable_path('python')),
            'uwsgi_executable': get_executable_path('uwsgi'),
            'celery_executable': get_executable_path('celery'),
            'watchdog_executable': get_executable_path('packy-watchdog'),
            'agent_name': AGENT_SUPERVISOR_NAME,
            'control_server_name': CONTROL_SERVER_SUPERVISOR_NAME,
            'watchdog_name': WATCHDOG_SUPERVISOR_NAME,
            'uwsgi_ini': configuration.get_uwsgi_configuration_file(),
            'is_inside_docker_container': is_inside_docker_container(),
        }

        content = render_template_from_package_file_content(
            'packy_agent.configuration', 'templates/supervisord.conf', context)

        write_to_console_or_file(configuration_file, content)

    def generate_uwsgi_ini(self, configuration_file=None, is_development=False):
        configuration_file = configuration_file or configuration.get_uwsgi_configuration_file()
        logger.info('Generating uWSGI configuration file content to %s', configuration_file)

        context = {
            'pid_file': configuration.get_uwsgi_pid_file(),
            'venv_dir': os.path.normpath(os.path.dirname(get_executable_path('python')) + '/..'),
            'is_development': is_development,
        }

        content = render_template_from_package_file_content(
            'packy_agent.configuration', 'templates/uwsgi.ini', context)

        write_to_console_or_file(configuration_file, content)

    def generate_nginx_conf(self, configuration_file=None):
        # TODO(dmu) LOW: Use symlink for nginx configuration file in `/etc/nginx/sites-enabled/`
        configuration_file = configuration_file or configuration.get_nginx_configuration_file()
        logger.info('Generating nginx configuration file content to %s', configuration_file)

        content = render_template_from_package_file_content(
            'packy_agent.configuration', 'templates/nginx.conf',
            {'control_server_port': configuration.get_control_server_port()})

        write_to_console_or_file(configuration_file, content)

    def create_auxiliary_directories(self):
        logger.info('Creating auxiliaary directories')

        directories = {
            os.path.dirname(configuration.get_supervisor_configuration_file()),
            configuration.get_supervisor_log_directory(),
            configuration.get_supervisor_run_directory(),
            os.path.dirname(configuration.get_uwsgi_pid_file()),
            os.path.dirname(configuration.get_control_server_stdout_log_file()),
            os.path.dirname(configuration.get_control_server_stderr_log_file()),
            os.path.dirname(configuration.get_agent_stdout_log_file()),
            os.path.dirname(configuration.get_agent_stderr_log_file()),
            os.path.dirname(configuration.get_watchdog_stdout_log_file()),
            os.path.dirname(configuration.get_watchdog_stderr_log_file()),
        }

        for directory in directories:
            try:
                logger.info('Creating %s', directory)
                os.makedirs(directory)
            except Exception:
                # TODO(dmu) LOW: Be more specific about catching exception
                # Forgive already existing directory
                continue

        if log2ram_service.is_active():
            # This makes log2ram service to dump logs from /var/log (RAM) to /var/log.hdd (SD card)
            # to have new directories properly persisted
            log2ram_service.reload()


install_and_upgrade_manager = InstallAndUpgradeManager()
