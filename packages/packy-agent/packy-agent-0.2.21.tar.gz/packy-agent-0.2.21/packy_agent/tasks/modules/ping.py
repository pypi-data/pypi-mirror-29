import logging

from celery import shared_task
from retry.api import retry_call

from packy_agent.clients.packy_server import packy_server_client_factory
from packy_agent.configuration.agent.base import configuration
from packy_agent.utils.ping import do_one as ping_once
from packy_agent.utils.misc import get_iso_format_utcnow

logger = logging.getLogger(__name__)


def ping(host):
    module_config = configuration.get_ping_module_configuration()

    start_time = get_iso_format_utcnow()
    pings = []
    number_of_pings = module_config['number_of_pings']
    packet_size = module_config['packet_size']
    for _ in xrange(number_of_pings):
        try:
            result = ping_once(host, 10, n_bytes=packet_size)
            if result:
                time_seconds, __ = result
            else:
                continue
        except Exception:
            logger.warning('Error during ping', exc_info=True)
            continue

        time_ms = round(time_seconds * 1000, 2)
        pings.append(time_ms)

    # TODO(dmu) HIGH: Producing of result structure should be moved to PackyServerClient level
    return {
        'target': host,
        'packet_size': packet_size,
        'n_pings': number_of_pings,
        'time': start_time,
        'pings': ','.join(map(str, pings))
    }


@shared_task
def ping_all():
    hosts = configuration.get_ping_module_configuration().get('hosts')
    if not hosts:
        logger.warning('Ping hosts are not configured')
        # TODO(dmu) HIGH: Should I mark task as failed?
        return

    client = packy_server_client_factory.get_client_by_configuration(configuration)
    # See comment for speedtest
    for host in hosts:
        result = ping(host)
        retry_call(client.submit_ping_measurement, (result,),
                   tries=configuration.get_submit_retries())
