import logging

from celery import shared_task
from retry.api import retry_call

from packy_agent.clients.packy_server import packy_server_client_factory
from packy_agent.configuration.agent.base import configuration
from packy_agent.utils.speedtest import run_speedtest
from packy_agent.utils.misc import get_iso_format_utcnow

MBIT = 1000000.0

logger = logging.getLogger(__name__)


def speedtest(host):
    start_time = get_iso_format_utcnow()
    results = run_speedtest(host)
    # TODO(dmu) HIGH: Producing of result structure should be moved to PackyServerClient level
    return {
        'target': host,
        'upload_speed': round(results.upload / MBIT, 2),
        'download_speed': round(results.download / MBIT, 2),
        'time': start_time,
        'ping': round(results.ping, 3)
    }


@shared_task
def speedtest_all():
    # TODO(dmu) HIGH: Reloading configuration file at every task run is a bad idea. Refactor
    hosts = configuration.get_speedtest_module_configuration().get('hosts')
    if not hosts:
        logger.warning('Speedtest hosts are not configured')
        # TODO(dmu) HIGH: Should I mark task as failed?
        return

    client = packy_server_client_factory.get_client_by_configuration(configuration)

    # Celery has limitations for creating subprocesses via multiprocessing
    # https://github.com/celery/celery/issues/1709 therefore we run speedtest measurement
    # sequentially
    for host in hosts:
        result = speedtest(host)
        retry_call(client.submit_speedtest_measurement, (result,),
                   tries=configuration.get_submit_retries())
