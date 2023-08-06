import logging
from urlparse import urlparse
import time
from datetime import datetime
import socket
import ssl


from packy_agent.models.measurement import HTTPModuleMeasurement


logger = logging.getLogger(__name__)


SSL_DT_FORMAT = r'%b %d %H:%M:%S %Y %Z'
CHROME_USERAGENT = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/56.0.2924.87 Safari/537.36')


def get_certificate_expiration_dt(url):
    url_parsed = urlparse(url)
    if url_parsed.scheme != 'https':
        return None

    parts = (url_parsed.netloc + ':443').split(':')
    hostname = parts[0]
    port = int(parts[1])

    context = ssl.create_default_context()
    connection = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
    connection.settimeout(5)

    connection.connect((hostname, port))
    ssl_info = connection.getpeercert()

    return datetime.strptime(ssl_info['notAfter'], SSL_DT_FORMAT)


def get_http_measurement(url, follow_redirects=False):
    logger.debug('Getting HTTP measurement for {}'.format(url))

    # We import here to allow install/upgrade procedure successfully install pycurl system library
    # dependencies
    import pycurl
    curl_object = pycurl.Curl()

    curl_object.setopt(pycurl.URL, url)
    curl_object.setopt(pycurl.USERAGENT, CHROME_USERAGENT)
    if follow_redirects:
        curl_object.setopt(pycurl.MAXREDIRS, 1)
        curl_object.setopt(pycurl.FOLLOWLOCATION, 1)

    curl_object.setopt(pycurl.WRITEFUNCTION, lambda dummy: None)
    measurement = HTTPModuleMeasurement({'ts': int(time.time()), 'target': url})
    try:
        curl_object.perform()
    except pycurl.error:
        measurement.is_success = False
        return measurement

    measurement.http_status_code = curl_object.getinfo(pycurl.RESPONSE_CODE)
    measurement.namelookup_ms = round(curl_object.getinfo(pycurl.NAMELOOKUP_TIME) * 1000, 2)
    measurement.total_ms = round(curl_object.getinfo(pycurl.TOTAL_TIME) * 1000, 2)

    try:
        measurement.certificate_expiration_dt = get_certificate_expiration_dt(url)
    except IOError:
        logger.exception('Error while getting certification expiration datetime')

    return measurement
