import logging

from celery import shared_task
from packy_agent.managers.install_and_upgrade import install_and_upgrade_manager


logger = logging.getLogger(__name__)


def install_impl(version=None):
    install_and_upgrade_manager.install_and_restart(version=version)


# TODO(dmu) MEDIUM: Remove `update_self`
@shared_task()
def update_self():
    install_impl()


@shared_task()
def upgrade():
    install_impl()


@shared_task()
def install(version):
    install_impl(version)
