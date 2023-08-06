import os
import os.path
import yaml

from packy_agent.utils.collections import deep_update

from packy_agent.configuration import common as common_configuration
from packy_agent.configuration.base import BaseConfiguration
from packy_agent.utils.pkg_resources import get_package_file_content
from packy_agent.utils.misc import generate_random_string


def generate_flask_secret_key():
    return generate_random_string(128)


class ControlServerConfiguration(BaseConfiguration):

    FLASK_CONFIGURATION_KEY = 'flask'
    CONTROL_SERVER_CONFIGURATION_KEY = 'control_server'
    SECRET_KEY_KEY = 'SECRET_KEY'

    def __init__(self):
        super(ControlServerConfiguration, self).__init__()

        self.flask_configuration = None
        self.control_server_configuration = None

        self.server_base_url = None

    def get_local_configuration_file_path(self):
        return (os.getenv(common_configuration.CONTROL_SERVER_CONFIG_ENVVAR_NAME) or
                common_configuration.DEFAULT_CONTROL_SERVER_CONFIG_PATH)

    def get_flask_configuration(self):
        was_updated = self.load_local_configuration()
        if was_updated or self.flask_configuration is None:
            flask_configuration = yaml.load(
                get_package_file_content('packy_agent.configuration.control_server',
                                         'flask.yaml'))
            deep_update(flask_configuration,
                        self.local_configuration.get(self.FLASK_CONFIGURATION_KEY) or {})

            secret_key_key = self.SECRET_KEY_KEY
            if not flask_configuration.get(secret_key_key):
                secret_key = generate_flask_secret_key()
                flask_configuration[secret_key_key] = secret_key
                self.local_configuration.setdefault(
                    self.FLASK_CONFIGURATION_KEY, {})[secret_key_key] = secret_key

                self.save_local_configuration()

            self.flask_configuration = flask_configuration

        return self.flask_configuration

    def get_control_server_configuration(self):
        was_updated = self.load_local_configuration()
        if was_updated or self.control_server_configuration is None:
            control_server_configuration = yaml.load(
                get_package_file_content('packy_agent.configuration.control_server',
                                         'custom.yaml'))
            deep_update(control_server_configuration,
                        (self.local_configuration.get(self.PACKY_CONFIGURATION_KEY) or {}).get(
                         self.CONTROL_SERVER_CONFIGURATION_KEY) or {})

            self.control_server_configuration = control_server_configuration
            self.override_server_base_url()

        return self.control_server_configuration

    def set_server_base_url_override(self, server_base_url):
        self.server_base_url = server_base_url

    def override_server_base_url(self, server_base_url=None):
        self.server_base_url = server_base_url or self.server_base_url

        self.control_server_configuration['server_base_url'] = (
            self.server_base_url or
            os.getenv(common_configuration.PACKY_SERVER_BASE_URL_ENVVAR_NAME) or
            self.control_server_configuration['server_base_url'] or
            common_configuration.DEFAULT_SERVER_BASE_URL
        )

    def get_server_base_url(self):
        return self.get_control_server_configuration().get('server_base_url')

    def get_supervisor_configuration_file(self):
        return self.get_control_server_configuration().get('supervisor_configuration_file')

    def get_uwsgi_configuration_file(self):
        return self.get_control_server_configuration().get('uwsgi_configuration_file')

    def get_nginx_configuration_file(self):
        return self.get_control_server_configuration().get('nginx_configuration_file')

    def get_supervisor_log_file(self):
        return self.get_control_server_configuration().get('supervisor_log_file')

    def get_supervisor_log_directory(self):
        return os.path.dirname(self.get_supervisor_log_file())

    def get_supervisor_run_directory(self):
        return self.get_control_server_configuration().get('supervisor_run_directory')

    def get_control_server_stdout_log_file(self):
        return self.get_control_server_configuration().get('control_server_stdout_log_file')

    def get_control_server_stderr_log_file(self):
        return self.get_control_server_configuration().get('control_server_stderr_log_file')

    def get_agent_stdout_log_file(self):
        return self.get_control_server_configuration().get('agent_stdout_log_file')

    def get_agent_stderr_log_file(self):
        return self.get_control_server_configuration().get('agent_stderr_log_file')

    def get_watchdog_stdout_log_file(self):
        return self.get_control_server_configuration().get('watchdog_stdout_log_file')

    def get_watchdog_stderr_log_file(self):
        return self.get_control_server_configuration().get('watchdog_stderr_log_file')

    def get_uwsgi_pid_file(self):
        return self.get_control_server_configuration().get('uwsgi_pid_file')

    def get_packy_agent_pypi_repository(self):
        return self.get_control_server_configuration().get('packy_agent_pypi_repository')

    def is_reboot_enabled(self):
        return self.get_control_server_configuration().get('enable_reboot')

    def is_upgrade_enabled(self):
        return self.get_control_server_configuration().get('enable_upgrade')

    def is_network_configuration_enabled(self):
        return self.get_control_server_configuration().get('enable_network_configuration')

    def get_network_interface(self):
        return self.get_control_server_configuration().get('network_interface')

    def get_interfaces_config_path(self):
        return self.get_control_server_configuration().get('interfaces_config_path')

    def is_debug_mode(self):
        return (self.get_control_server_configuration().get('is_debug_mode') or
                super(ControlServerConfiguration, self).is_debug_mode())

    def get_control_server_port(self):
        return self.get_control_server_configuration().get('http_port')

    def set_control_server_port(self, port):
        self.load_local_configuration()
        self.local_configuration.setdefault('packy', {}).setdefault(
            'control_server', {})['http_port'] = port
        self.save_local_configuration()


configuration = ControlServerConfiguration()
