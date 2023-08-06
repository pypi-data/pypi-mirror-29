import logging
import re
import signal

from io import BytesIO
from subprocess import call


import supervisor.supervisorctl
from supervisor.options import ClientOptions

from packy_agent.configuration.control_server.base import configuration as control_server_configuration
from packy_agent.configuration.agent.base import configuration as agent_configuration
# TODO(dmu) MEDIUM: Use common code to restart supervisor from `packy-server`
from packy_agent.utils.misc import run_shell_command_async, get_executable_path

AGENT_SUPERVISOR_NAME = 'agent'
CONTROL_SERVER_SUPERVISOR_NAME = 'control-server'
WATCHDOG_SUPERVISOR_NAME = 'watchdog'
NGINX_SUPERVISOR_NAME = 'nginx'

AGENT_STATUS_RE = re.compile('^' + AGENT_SUPERVISOR_NAME + r' +([A-Z]+)(.*)$')
AGENT_UPTIME_RE = re.compile('^ +pid \d+, uptime (.*)$')

logger = logging.getLogger(__name__)


def supervisor_main(args=None, options=None, stdout=None):
    if options is None:
        options = ClientOptions()

    options.realize(args, doc=__doc__)
    c = supervisor.supervisorctl.Controller(options, stdout=stdout)

    if options.args:
        c.onecmd(' '.join(options.args))

    if options.interactive:
        c.exec_cmdloop(args, options)


def run_supervisor_command_sync(command, *args):
    logger.debug('Running sync supervisor command: %s %s', command, args)
    stdout = BytesIO()
    supervisor_main(
        ['-c', control_server_configuration.get_supervisor_configuration_file(), command] + list(args),
        stdout=stdout)

    stdout.seek(0)
    return stdout.read().decode('utf-8')


def get_supervisor_shell_command(command, args):
    args = (command,) + args
    return '{} -c {} {}'.format(get_executable_path('supervisorctl'),
        control_server_configuration.get_supervisor_configuration_file(), ' '.join(args))


def get_control_server_restart_shell_command():
    try:
        with open(control_server_configuration.get_uwsgi_pid_file()) as f:
            uwsgi_pid = int(f.read())
    except Exception:
        logger.warning('Unable to get uWSGI pid')
        return

    return 'kill -{} {}'.format(signal.SIGHUP, uwsgi_pid)


def run_supervisor_command_async(command, args, delay_seconds=None, dev_null=False):
    logger.debug('Running async supervisor command: %s %s', command, args)
    shell_command = get_supervisor_shell_command(command, args)
    run_shell_command_async(shell_command, delay_seconds, dev_null=dev_null)


def run_supervisor_command(command, args, delay_seconds=None, async=False, dev_null=False):
    if delay_seconds is None and not async:
        return run_supervisor_command_sync(command, *args)
    else:
        return run_supervisor_command_async(command, args, delay_seconds=delay_seconds,
                                            dev_null=dev_null)


class ControlManager(object):

    def reboot(self, delay_seconds=None):
        agent_configuration.set_stopped(False)
        if control_server_configuration.is_reboot_enabled():
            if delay_seconds is None:
                call(['reboot', 'now'])
            else:
                run_shell_command_async('reboot now', delay_seconds=delay_seconds)
        else:
            logger.info('Reboot was disabled (for developer protection)')

    def restart_packy_agent(self, delay_seconds=None, dev_null=False):
        # TODO(dmu) HIGH: Restart Packy Agent asynchronously?
        # TODO(dmu) MEDIUM: Use common code to restart supervisor from `packy-server`
        logger.debug('Restarting agent...')
        agent_configuration.set_stopped(False)
        run_supervisor_command('restart', (AGENT_SUPERVISOR_NAME,), delay_seconds=delay_seconds,
                               dev_null=dev_null)

    def restart_watchdog(self, delay_seconds=None):
        logger.debug('Restarting watchdog...')
        run_supervisor_command('restart', (WATCHDOG_SUPERVISOR_NAME,), delay_seconds=delay_seconds)

    def restart_nginx(self, delay_seconds=None):
        logger.debug('Restarting nginx...')
        run_supervisor_command('restart', (NGINX_SUPERVISOR_NAME,), delay_seconds=delay_seconds)

    def start_packy_agent(self):
        logger.debug('Starting agent...')
        agent_configuration.set_stopped(False)
        run_supervisor_command_sync('start', AGENT_SUPERVISOR_NAME)

    def stop_packy_agent(self):
        logger.debug('Stopping agent...')
        agent_configuration.set_stopped(True)
        run_supervisor_command_sync('stop', AGENT_SUPERVISOR_NAME)

    def restart_control_server(self, delay_seconds=None):
        logger.debug('Restarting control server...')
        command = get_control_server_restart_shell_command()
        if command:
            run_shell_command_async(command, delay_seconds=delay_seconds)
        # TODO(dmu) MEDIUM: `uwsgi.reload()` breaks current request and we do not manage to send
        #                   response to user
        # import uwsgi
        # uwsgi.reload()
        # TODO(dmu) MEDIUM: Restart via supervisor does not work properly under Docker, because
        #                   supervisord under Docker kills background subprocess that runs
        #                   restart procedure (maybe it is Alpine specific)
        # run_supervisor_command('restart', (CONTROL_SERVER_SUPERVISOR_NAME,),
        #                        delay_seconds=delay_seconds)

    def restart(self, delay_seconds=None):
        """Restart all components"""
        logger.debug('Restarting all components...')
        self.restart_packy_agent()
        self.restart_watchdog()
        self.restart_nginx()
        self.restart_control_server(delay_seconds=delay_seconds)
        # TODO(dmu) MEDIUM: Restart via supervisor does not work properly under Docker, because
        #                   supervisord under Docker kills background subprocess that runs
        #                   restart procedure (maybe it is Alpine specific)
        # run_supervisor_command('restart', ('all',), delay_seconds=delay_seconds)

    def get_packy_agent_status(self):
        status = None
        uptime = None

        output = run_supervisor_command_sync('status', AGENT_SUPERVISOR_NAME)
        output = output.rstrip()
        match_status = AGENT_STATUS_RE.match(output)
        if match_status:
            status, tail = match_status.groups()
            match_uptime = AGENT_UPTIME_RE.match(tail)
            if match_uptime:
                 uptime = match_uptime.group(1)

        return status, uptime


control_manager = ControlManager()
