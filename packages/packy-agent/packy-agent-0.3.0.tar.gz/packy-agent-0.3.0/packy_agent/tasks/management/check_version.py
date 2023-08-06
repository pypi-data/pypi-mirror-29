from celery import shared_task

import packy_agent


# TODO(dmu) HIGH: Do we need this task now? Version is being sent with each heartbeat
@shared_task()
def check_version():
    return packy_agent.__version__
