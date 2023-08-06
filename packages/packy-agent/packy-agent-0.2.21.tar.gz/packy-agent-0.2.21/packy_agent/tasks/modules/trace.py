import logging

from retry.api import retry_call

from celery import shared_task
from celery.signals import task_postrun

from packy_agent.clients.packy_server import packy_server_client_factory
from packy_agent.configuration.agent.base import configuration
from packy_agent.utils.traceroute.base import traceroute
from packy_agent.utils.misc import get_iso_format_utcnow


logger = logging.getLogger(__name__)


def convert_to_hops(traceroute_result, ping_count):
    hops = []
    for x, item in enumerate(traceroute_result):
        hop = {
            'host': item['host'],
            'number': x + 1,
            'loss': round(100.0 * item['loss'] / ping_count, 1),
            'sent': ping_count,
        }
        for attr in ('last', 'average', 'best', 'worst', 'stdev'):
            value = item.get(attr)
            if value is not None:
                hop[attr] = round(value * 1000.0, 1)

        hops.append(hop)

    return hops


def trace(host):
    module_config = configuration.get_trace_module_configuration()

    start_time = get_iso_format_utcnow()
    ping_count = module_config['number_of_pings']
    result = traceroute(host, ping_count=ping_count, max_hops=module_config['ttl'])
    # TODO(dmu) HIGH: Producing of result structure should be moved to PackyServerClient level
    return {
        'target': host,
        'TOS': '0x0',  # TODO(dmu) LOW: Do we need to send it?
        'packet_size': module_config['packet_size'],
        'bitpattern': '0x00',  # TODO(dmu) LOW: Do we need to send it?
        'pings': module_config['number_of_pings'],
        'time': start_time,
        'hops': convert_to_hops(result, ping_count),
    }


@shared_task
def trace_all():
    hosts = configuration.get_trace_module_configuration().get('hosts')
    if not hosts:
        logger.warning('Trace hosts are not configured')
        # TODO(dmu) HIGH: Should I mark task as failed?
        return

    client = packy_server_client_factory.get_client_by_configuration(configuration)
    # See comment for speedtest
    for host in hosts:
        result = trace(host)
        retry_call(client.submit_trace_measurement, (result,),
                   tries=configuration.get_submit_retries())


# TODO(dmu) HIGH: Replace this work-around with a solution. Probably after refactoring Celery-based
#                 architecture
# We need shutdown worker after trace task because it does `gevent` patching for `socket` module
# and only known way to unpatch for now is `reload(socket)`. This makes storing different object
# into `socket._GLOBAL_DEFAULT_TIMEOUT` (because it assigned on module load) which differs from
# object used in other modules (we had it before reload). For example in httplib:
# HTTPConnection(..., timeout=socket._GLOBAL_DEFAULT_TIMEOUT,...)
def shutdown_worker(**kwargs):
    logger.debug('Exiting worker to prevent `socket` module reload mess')
    raise SystemExit()

task_postrun.connect(shutdown_worker, sender=trace_all)
