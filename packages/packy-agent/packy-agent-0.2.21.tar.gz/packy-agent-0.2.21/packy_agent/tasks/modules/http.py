import logging
from retry.api import retry_call

from celery import shared_task

from packy_agent.clients.packy_server import packy_server_client_factory
from packy_agent.configuration.agent.base import configuration
from packy_agent.modules.http.base import get_http_measurement
from packy_agent.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)


@shared_task
def http():
    module_config = configuration.get_http_module_configuration()
    if not module_config:
        raise ImproperlyConfigured('No configuration for `http` module found')

    urls = module_config.get('urls')
    if not urls:
        raise ImproperlyConfigured('URLs are not configured for `http` module')

    follow_redirects = module_config.get('follow_redirects', False)

    client = packy_server_client_factory.get_client_by_configuration(configuration)
    for url in urls:

        # TODO(dmu) MEDIUM: Figure out what happens inside `curl` library and remove this
        #                   workaround
        for _ in xrange(10):
            measurement = get_http_measurement(url, follow_redirects=follow_redirects)
            if measurement.total_ms < 4000000 and measurement.namelookup_ms < 4000000:
                break
        else:
            logger.error('Failed to get proper measurement from curl for {]'.format(url))
            continue

        measurement_json = measurement.to_primitive()
        retry_call(client.submit_http_measurement, (measurement_json,),
                   tries=configuration.get_submit_retries())
