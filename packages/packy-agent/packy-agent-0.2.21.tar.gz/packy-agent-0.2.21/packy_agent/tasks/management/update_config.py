import logging

from celery import shared_task

from packy_agent.configuration.agent.base import configuration

logger = logging.getLogger(__name__)


@shared_task()
def update_config():
    configuration.update_local_configuration_from_server()
