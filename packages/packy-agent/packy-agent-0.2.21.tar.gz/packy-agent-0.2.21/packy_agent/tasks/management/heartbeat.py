import logging
import json
import os.path

from celery import shared_task

import psutil

import packy_agent
from packy_agent.clients.packy_server import packy_server_client_factory
from packy_agent.configuration.agent.base import configuration
from packy_agent.managers.network import network_manager
from packy_agent.utils.misc import atomic_write

logger = logging.getLogger(__name__)


def load_data_usage():
    filename = configuration.get_data_usage_file()
    try:
        with open(filename, 'r') as f:
            content = f.read()
            if content:
                content_json = json.loads(content)
                return content_json.get('bytes_sent'), content_json.get('bytes_received')
    except IOError:
        pass

    return None, None


def set_data_usage(bytes_sent, bytes_received):
    with atomic_write(configuration.get_data_usage_file(), overwrite=True) as f:
        f.write(json.dumps({'bytes_sent': bytes_sent, 'bytes_received': bytes_received}))


def get_data_usage():
    snetio = psutil.net_io_counters(pernic=True, nowrap=True)
    snetio.pop('lo', None)

    bytes_sent = 0
    bytes_received = 0

    for value in snetio.itervalues():
        bytes_sent += value.bytes_sent
        bytes_received += value.bytes_recv

    return bytes_sent, bytes_received


@shared_task()
def heartbeat():
    if not configuration.is_heartbeat_enabled():
        logger.debug('Heartbeat is disabled')
        return

    prev_bytes_sent, prev_bytes_received = load_data_usage()
    bytes_sent, bytes_received = get_data_usage()
    set_data_usage(bytes_sent, bytes_received)

    client = packy_server_client_factory.get_client_by_configuration(configuration)
    try:
        client.update_status(version=packy_agent.__version__,
                             ip_address=network_manager.get_actual_ip_address(),
                             prev_bytes_sent=prev_bytes_sent,
                             prev_bytes_received=prev_bytes_received,
                             bytes_sent=bytes_sent,
                             bytes_received=bytes_received)
    except Exception:
        logger.warning('Error while sending heartbeat', exc_info=True)
