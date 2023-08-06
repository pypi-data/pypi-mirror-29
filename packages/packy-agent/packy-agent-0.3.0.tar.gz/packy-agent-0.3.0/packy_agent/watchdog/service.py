import time
import logging
import signal

from uptime import uptime
import psutil

from packy_agent.configuration.agent.base import configuration as agent_configuration
from packy_agent.configuration.control_server.base import configuration as cs_configuration
from packy_agent.clients.packy_server import packy_server_client_factory
from packy_agent.utils.misc import to_epoch, iso_to_datetime, is_inside_docker_container
from packy_agent.managers.control import control_manager
from packy_agent.managers.install_and_upgrade import install_and_upgrade_manager

logger = logging.getLogger(__name__)


FAILOVER_CHECK_PERIOD_SECONDS = 30
ROOT_PID = 1


def custom_uptime():
    if is_inside_docker_container():
        process = psutil.Process(ROOT_PID)
        return time.time() - process.create_time()
    else:
        return uptime()


class WatchdogService(object):

    def __init__(self):
        self._graceful_stop = False

        self.known_activated_time = None
        self.last_restart_time = None
        self.last_known_online_time = None

    def graceful_stop(self):
        self._graceful_stop = True

    def get_last_online_time(self):
        last_online_dt = None
        try:
            client = packy_server_client_factory.get_client_by_configuration(agent_configuration)
            response = client.get_agent()
            body_json = response.json()
            last_online_dt = body_json.get('last_online_dt')
        except Exception:
            logger.exception('Error while getting online time')

        if last_online_dt:
            last_online_time = to_epoch(iso_to_datetime(last_online_dt))
            self.last_known_online_time = last_online_time
            return last_online_time
        else:
            if self.last_known_online_time is None:
                return self.known_activated_time
            else:
                return self.last_known_online_time

    def get_offline_period(self):
        return time.time() - self.get_last_online_time()

    def notify_server(self):
        base_url = cs_configuration.get_server_base_url()

        client = packy_server_client_factory.get_client(base_url)
        control_server_url = install_and_upgrade_manager.get_control_server_link(base_url)
        client.notify_server(control_server_url)

    def loop_iteration(self):
        if not agent_configuration.is_activated():
            logger.info('Agent is not activated')
            self.notify_server()
            return

        if agent_configuration.is_stopped():
            logger.info('Agent is stopped on purpose')
            return

        if self.known_activated_time is None:
            self.known_activated_time = time.time()

        offline_period = self.get_offline_period()
        watchdog_config = agent_configuration.get_watchdog_configuration()
        if watchdog_config['max_offline_period_before_reboot_seconds'] < offline_period:
            if custom_uptime() >= watchdog_config['reboot_period_seconds']:
                control_manager.reboot()
                return

        if watchdog_config['max_offline_period_before_restart_seconds'] < offline_period:
            if (not self.last_restart_time or
                    (time.time() - self.last_restart_time) >=
                        watchdog_config['restart_period_seconds']):
                self.last_restart_time = time.time()
                control_manager.restart_packy_agent()
                return

    def run(self):
        # TODO(dmu) HIGH: Improve logging configuration
        logging.basicConfig(format='%(asctime)-15s %(levelname)s [%(name)s]: %(message)s',
                            level=logging.DEBUG)

        logger.info('Watchdog started')
        signal.signal(signal.SIGTERM, lambda signum, frame: self.graceful_stop())
        while not self._graceful_stop:
            start = time.time()
            try:
                self.loop_iteration()
            except Exception:
                logger.exception('Error during loop iteration')

            try:
                check_period_seconds = agent_configuration.get_watchdog_configuration(
                    )['check_period_seconds']
            except Exception:
                check_period_seconds = FAILOVER_CHECK_PERIOD_SECONDS
                logger.exception('Could not get check period seconds from configuration file, '
                                 'using failover value: %s', check_period_seconds)
            wait_duration = check_period_seconds - (time.time() - start)
            if wait_duration > 0:
                logger.debug('Waiting for %s seconds for next iteration', wait_duration)
                time.sleep(wait_duration)

        logger.info('Watchdog gracefully stopped')
