import logging

from celery import shared_task
from packy_agent.managers.control import control_manager


logger = logging.getLogger(__name__)


@shared_task()
def restart():
    control_manager.restart_packy_agent(delay_seconds=2)
