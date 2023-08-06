import logging
import os
import os.path

from packy_agent.managers.network import INTERFACES_CONFIG_PATH, BACKUP_FILENAME_TEMPLATE
from packy_agent.configuration.agent.base import configuration as agent_configuration
from packy_agent.configuration.control_server.base import configuration as control_server_configuration
from packy_agent.utils.misc import is_inside_docker_container


logger = logging.getLogger(__name__)


class ResetManager(object):

    def reset_network_configuration(self):
        if control_server_configuration.is_network_configuration_enabled():
            backup_file = BACKUP_FILENAME_TEMPLATE.format(INTERFACES_CONFIG_PATH)
            try:
                os.rename(backup_file, INTERFACES_CONFIG_PATH)
            except Exception as ex:
                logger.warning('Network configuration was not restored: %s', ex)
        else:
            logger.info('Network configuration change was disabled (for developer protection)')

    def reset_agent_activation(self):
        # We are doing deactivate() as a defensive programming measure to avoid accident
        # overwriting deleted file with configuration from memory
        agent_configuration.deactivate()

        # We remove file to be closer to fresh install state
        file_path = agent_configuration.get_local_configuration_file_path()
        logger.info('Removing configuration file: %s', file_path)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except Exception:
                logger.exception('Error while removing configuration file: %s', file_path)

    def reset(self):
        if not is_inside_docker_container():
            self.reset_network_configuration()

        self.reset_agent_activation()

reset_manager = ResetManager()
