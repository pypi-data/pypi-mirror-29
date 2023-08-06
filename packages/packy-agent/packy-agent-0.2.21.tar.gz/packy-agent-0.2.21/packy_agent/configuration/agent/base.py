import os
import logging
import yaml

from kombu import Queue, Exchange
from kombu.common import Broadcast

from packy_agent.utils.collections import deep_update

from packy_agent.configuration import common as common_configuration
from packy_agent.configuration.base import BaseConfiguration
from packy_agent.exceptions import ImproperlyConfigured
from packy_agent.utils.pkg_resources import get_package_file_content
from packy_agent.utils.network import get_hostname_from_url
from packy_agent.clients.packy_server import packy_server_client_factory


logger = logging.getLogger(__name__)


class PackyAgentConfiguration(BaseConfiguration):

    CELERY_CONFIGURATION_KEY = 'celery'
    AGENT_CONFIGURATION_KEY = 'agent'

    def __init__(self):
        super(PackyAgentConfiguration, self).__init__()

        self.celery_configuration = None
        self.packy_agent_configuration = None

    def update_local_configuration_from_server(self):
        logger.info('Updating configuration file...')
        agent_id = configuration.get_agent_id()
        if agent_id is None:
            logger.error('Could not update config, because Packy Agent ID (packy.agent.agent_id) '
                         'is not known')
            return

        client = packy_server_client_factory.get_client_by_configuration(configuration)
        response = client.get_agent_config(agent_id)

        if response.status_code == 200:
            self.save_local_configuration(content=response.content)
            # TODO(dmu) HIGH: If Celery related configuration is updated, for example `broker_url`
            #                 then Celery should be restarted
        else:
            logger.error('Error while updating config: HTTP%s %s',
                         response.status_code, response.content)

    def get_local_configuration_file_path(self):
        return (os.getenv(common_configuration.AGENT_CONFIG_ENVVAR_NAME) or
                common_configuration.DEFAULT_AGENT_CONFIG_PATH)

    def get_celery_configuration(self):
        was_updated = self.load_local_configuration()
        if was_updated or self.celery_configuration is None:
            agent_id = self.get_agent_id()
            if agent_id is None:
                raise ImproperlyConfigured('Packy Agent id (packy.agent.agent_id) is not set,'
                                           'unable to get celery configuration')

            celery_configuration = yaml.load(
                get_package_file_content('packy_agent.configuration.agent', 'celery.yaml'))
            deep_update(celery_configuration,
                        self.local_configuration[self.CELERY_CONFIGURATION_KEY])

            # TODO(dmu) HIGH: This is for compatibility reasons, remove it once Packy Server is
            #                 upgraded to v0.0.13
            if self.local_configuration[self.CELERY_CONFIGURATION_KEY].get('broker_url') is None:
                broker_url = self.local_configuration.get('broker_url')
                if broker_url is not None:
                    celery_configuration['broker_url'] = broker_url

            str_agent_id = str(agent_id)
            celery_configuration['task_default_queue'] = str_agent_id
            celery_configuration['task_default_routing_key'] = str_agent_id
            celery_configuration['task_queues'] = (
                Queue(str_agent_id,
                      Exchange(celery_configuration['task_default_exchange'], delivery_mode=1),
                      routing_key=str_agent_id, auto_delete=True, durable=False,
                      queue_arguments={'x-message-ttl': 10000}),
                Broadcast('broadcast_tasks', auto_delete=True, durable=False, exclusive=True,
                          delivery_mode=1,
                          queue_arguments={'x-message-ttl': 10000, 'x-expires': 10000}),
            )

            self.celery_configuration = celery_configuration

        return self.celery_configuration

    def get_packy_agent_configuration(self):
        was_updated = self.load_local_configuration()
        if was_updated or self.packy_agent_configuration is None:
            packy_agent_configuration = yaml.load(
                get_package_file_content('packy_agent.configuration.agent', 'custom.yaml'))
            deep_update(packy_agent_configuration,
                        (self.local_configuration.get(self.PACKY_CONFIGURATION_KEY) or {}).get(
                         self.AGENT_CONFIGURATION_KEY) or {})

            self.packy_agent_configuration = packy_agent_configuration

        return self.packy_agent_configuration

    def get_watchdog_configuration(self):
        return self.get_packy_agent_configuration()['watchdog']

    def get_server_base_url(self):
        # TODO(dmu) HIGH: It is strange that we use slightly different way to get `server_base_url`
        #                 for bootstrap server and packy agent
        return self.get_packy_agent_configuration().get('server_base_url')

    def get_server_hostname(self):
        return get_hostname_from_url(self.get_server_base_url())

    def get_agent_id(self):
        return self.get_packy_agent_configuration().get('agent_id')

    def get_client_id(self):
        return self.get_packy_agent_configuration().get('client_id')

    def get_client_secret(self):
        return self.get_packy_agent_configuration().get('client_secret')

    def is_activated(self):
        return (self.get_agent_id() is not None and self.get_client_id() is not None and
                self.get_client_secret() is not None)

    def deactivate(self):
        self.load_local_configuration()
        config = self.local_configuration.setdefault('packy', {}).setdefault('agent', {})

        config['agent_id'] = None
        config['client_id'] = None
        config['client_secret'] = None
        self.save_local_configuration()

    def get_tasks_prefix(self):
        return self.get_packy_agent_configuration().get('tasks_prefix')

    def get_module_configuration(self, module_public_identifier):
        return (self.get_packy_agent_configuration().get('modules') or {}).get(
            module_public_identifier)

    def get_ping_module_configuration(self):
        return self.get_module_configuration('ping')

    def get_trace_module_configuration(self):
        return self.get_module_configuration('trace')

    def get_speedtest_module_configuration(self):
        return self.get_module_configuration('speedtest')

    def get_http_module_configuration(self):
        return self.get_module_configuration('http')

    def is_debug_mode(self):
        return (self.get_packy_agent_configuration().get('is_debug_mode') or
                super(PackyAgentConfiguration, self).is_debug_mode())

    def set_stopped(self, value):
        # TODO(dmu) MEDIUM: This is not 100% consistent solution. If configuration file get updated
        #                   from server `is_stopped` flag will be removed. To address this we need
        #                   either: 1) save `is_stopped` to server 2) have another storage (config
        #                   file or local database) to store data that cannot be overwritten from
        #                   server
        self.load_local_configuration()
        self.local_configuration.setdefault('packy', {}).setdefault(
            'agent', {})['is_stopped'] = value
        self.save_local_configuration()

    def is_stopped(self):
        return self.get_packy_agent_configuration().get('is_stopped')

    def is_heartbeat_enabled(self):
        return self.get_packy_agent_configuration().get('is_heartbeat_enabled')

    def get_submit_retries(self):
        return self.get_packy_agent_configuration().get('submit_retries')

    def get_data_usage_file(self):
        return self.get_packy_agent_configuration().get('data_usage_file')


configuration = PackyAgentConfiguration()
