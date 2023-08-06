import logging
import time
import base64
import socket
import uuid
from urlparse import urljoin

import cachetools
import requests

import packy_agent
from packy_agent.exceptions import AuthenticationError
from packy_agent.utils.collections import set_if

packy_server_client = None
logger = logging.getLogger(__name__)


USER_AGENT = 'packy-agent/{}'.format(packy_agent.__version__)
DEFAULT_TIMEOUT = 15


def make_basic_auth_headers(username, password):
    return {'Authorization': 'Basic ' + base64.b64encode('%s:%s' % (username, password))}


class PackyServerClient(object):
    # TODO(dmu) HIGH: Implement support for persistent HTTP?

    OAUTH_TOKEN_PATH = 'oauth/token/'

    PENDING_AGENT_PATH = 'api/v2/pending-agent/'
    AGENT_VERSION_PATH = 'api/v2/agent-version/'
    AGENT_TEMPLATE_PATH = 'api/v2/user/agent/'
    AGENT_INSTANCE_TEMPLATE_PATH = AGENT_TEMPLATE_PATH + '{}/'

    UPDATE_STATUS_TEMPLATE_PATH = AGENT_INSTANCE_TEMPLATE_PATH
    AGENT_CONFIG_TEMPLATE_PATH = AGENT_INSTANCE_TEMPLATE_PATH + 'config/'
    VALIDATE_AUTH_TEMPLATE_PATH = AGENT_INSTANCE_TEMPLATE_PATH + 'validate-auth/'
    HEARTBEAT_TEMPLATE_PATH = AGENT_INSTANCE_TEMPLATE_PATH + 'heartbeat/'

    PING_MEASUREMENT_TEMPLATE_PATH = AGENT_INSTANCE_TEMPLATE_PATH + 'module/ping/measurement/'
    SPEEDTEST_MEASUREMENT_TEMPLATE_PATH = AGENT_INSTANCE_TEMPLATE_PATH + 'module/speedtest/measurement/'
    TRACE_MEASUREMENT_TEMPLATE_PATH = AGENT_INSTANCE_TEMPLATE_PATH + 'module/trace/measurement/'
    HTTP_MEASUREMENT_TEMPLATE_PATH = AGENT_INSTANCE_TEMPLATE_PATH + 'module/http/measurement/'

    def __init__(self, base_url, client_id=None, client_secret=None, agent_id=None,
                 timeout=DEFAULT_TIMEOUT):
        self.base_url = base_url

        self.client_id = client_id
        self.client_secret = client_secret
        self.agent_id = agent_id
        self.timeout = timeout

        self.token = None
        self.token_type = None
        self.token_expiration = None

        self.oauth_token_url = urljoin(base_url, self.OAUTH_TOKEN_PATH)
        self.pending_agent_url = urljoin(base_url, self.PENDING_AGENT_PATH)

        self.agent_version_url = urljoin(base_url, self.AGENT_VERSION_PATH)
        self.agent_config_template_url = urljoin(base_url, self.AGENT_CONFIG_TEMPLATE_PATH)

        self.create_agent_url = urljoin(base_url, self.AGENT_TEMPLATE_PATH)

        self.agent_template_url = urljoin(base_url, self.AGENT_INSTANCE_TEMPLATE_PATH)
        self.update_status_template_url = urljoin(base_url, self.UPDATE_STATUS_TEMPLATE_PATH)
        self.validate_auth_template_url = urljoin(base_url, self.VALIDATE_AUTH_TEMPLATE_PATH)

        self.ping_measurement_template_url = urljoin(base_url, self.PING_MEASUREMENT_TEMPLATE_PATH)
        self.speedtest_measurement_template_url = urljoin(base_url, self.SPEEDTEST_MEASUREMENT_TEMPLATE_PATH)
        self.trace_measurement_template_url = urljoin(base_url, self.TRACE_MEASUREMENT_TEMPLATE_PATH)
        self.http_measurement_template_url = urljoin(base_url, self.HTTP_MEASUREMENT_TEMPLATE_PATH)

        self.heartbeat_template_url = urljoin(base_url, self.HEARTBEAT_TEMPLATE_PATH)

    def set_client_id(self, client_id):
        self.client_id = client_id

    def set_client_secret(self, client_secret):
        self.client_secret = client_secret

    def request(self, url, data=None, json=None, method=None):
        if not method:
            if data or json:
                method = 'POST'
            else:
                method = 'GET'

        # TODO(dmu) HIGH: Implement token expiration support
        if not self.token or time.time() >= self.token_expiration:
            self.login()

        headers = {
            'Authorization': self.token_type + ' ' + self.token,
            'Content-Type': 'application/json',
            'User-Agent': USER_AGENT
        }

        tries = 2
        while tries > 0:
            tries -= 1
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=self.timeout)
            elif method == 'POST':
                response = requests.post(url, data=data, json=json, headers=headers,
                                         timeout=self.timeout)
            elif method == 'PATCH':
                response = requests.patch(url, data=data, json=json, headers=headers,
                                          timeout=self.timeout)
            else:
                raise NotImplementedError('Method {} is not supported'.format(method))

            if response.status_code == 401:
                # TODO(dmu) MEDIUM: Provide a better error response for expired token
                logger.debug('Maybe token has expired, will login again and retry: HTTP%s %s',
                             response.status_code, response.content)
                # TODO(dmu) MEDIUM: Support for exchange token or maybe switch to JWT
                self.login()
            else:
                break

        if response.status_code >= 400:
            logger.debug('HTTP%s: %s', response.status_code, response.content)

        return response

    def get_version_max(self):
        # TODO(dmu) LOW: Why do not we use self.request() or refactor?
        response = requests.get(self.agent_version_url, timeout=self.timeout)
        return response.json().get('version_max')

    def login(self):
        url = urljoin(self.base_url, self.OAUTH_TOKEN_PATH)
        response = requests.post(url,
                                 data={'grant_type': 'client_credentials',
                                       'client_id': self.client_id,
                                       'client_secret': self.client_secret},
                                 timeout=self.timeout)
        if response.status_code == 200:
            response_json = response.json()
            self.token = response_json['access_token']
            self.token_type = response_json['token_type']
            # expire earlier
            self.token_expiration = time.time() + response_json['expires_in'] * 0.9
        else:
            raise AuthenticationError('Not authenticated: %s', response.content)

    def activate_agent(self, email, password):
        headers = make_basic_auth_headers(email, password)
        headers['Content-Type'] = 'application/json'
        headers['User-Agent'] = USER_AGENT

        payload = {
            # TODO(dmu) MEDIUM: What `key` is used for?
            # TODO(dmu) LOW: Why not UUID4?
            'key': uuid.uuid1().hex,
            'name': socket.gethostname()
        }

        return requests.post(self.create_agent_url, json=payload,
                             headers=make_basic_auth_headers(email, password),
                             timeout=self.timeout)

    def validate_auth(self, username, password, agent_id):
        response = requests.post(self.validate_auth_template_url.format(agent_id),
                                 headers=make_basic_auth_headers(username, password),
                                 timeout=self.timeout)
        status_code = response.status_code
        if status_code == 401:
            return False

        if status_code == 404:
            logger.info('HTTP404: Probably credentials of %s do not match agent_id: %s',
                        username, agent_id)
            return False

        response.raise_for_status()
        return True

    def get_agent(self):
        return self.request(self.agent_template_url.format(self.agent_id))

    def get_agent_config(self, agent_id=None):
        # TODO(dmu) MEDIUM: Use only `self.agent_id`
        url = self.agent_config_template_url.format(agent_id or self.agent_id)
        return self.request(url)

    def notify_server(self, agent_control_server_url):
        # TODO(dmu) LOW: Why do not we use self.request() or refactor?
        response = requests.post(self.pending_agent_url,
                                 json={'agent_control_server_url': agent_control_server_url},
                                 timeout=self.timeout)
        response.raise_for_status()

    def submit_ping_measurement(self, data):
        return self.request(self.ping_measurement_template_url.format(self.agent_id), json=data)

    def submit_speedtest_measurement(self, data):
        return self.request(self.speedtest_measurement_template_url.format(self.agent_id),
                            json=data)

    def submit_trace_measurement(self, data):
        return self.request(self.trace_measurement_template_url.format(self.agent_id), json=data)

    def submit_http_measurement(self, data):
        return self.request(self.http_measurement_template_url.format(self.agent_id), json=data)

    def send_heartbeat(self):
        return self.request(self.heartbeat_template_url.format(self.agent_id), method='POST')

    def update_status(self, version=None, ip_address=None, is_online=True,
                      bytes_sent=None, prev_bytes_sent=None, bytes_received=None,
                      prev_bytes_received=None):
        payload = {'is_online': is_online}
        set_if(payload, 'version', version)
        set_if(payload, 'ip_address', ip_address)
        set_if(payload, 'bytes_sent', bytes_sent, if_callable=lambda x: x is not None)
        set_if(payload, 'prev_bytes_sent', prev_bytes_sent, if_callable=lambda x: x is not None)
        set_if(payload, 'bytes_received', bytes_received, if_callable=lambda x: x is not None)
        set_if(payload, 'prev_bytes_received', prev_bytes_received,
               if_callable=lambda x: x is not None)

        return self.request(self.update_status_template_url.format(self.agent_id),
                            json=payload, method='PATCH')


class PackyServerClientFactory(object):
    # This factory is needed because potentially configuration may change with configuration
    # update and we may need to login again to server

    def __init__(self):
        # We could implement differently taking in account that at the moment we need only one
        # client, but it would result in the code of the same complexity, but less flexible
        self.clients = cachetools.LRUCache(1)

    def get_client(self, base_url, client_id=None, client_secret=None, agent_id=None):
        key = (base_url, client_id, client_secret, agent_id)
        client = self.clients.get(key)

        if client:
            # It is not expected that someone modifies these attributes for factory acquired clients
            assert client.base_url == base_url
            assert client.client_id == client_id
            assert client.client_secret == client_secret
            assert client.agent_id == agent_id
        else:
            client = PackyServerClient(base_url=base_url, client_id=client_id,
                                       client_secret=client_secret, agent_id=agent_id)
            self.clients[key] = client

        return client

    def get_client_by_configuration(self, configuration):
        return self.get_client(
            base_url=configuration.get_server_base_url(),
            client_id=configuration.get_client_id(),
            client_secret=configuration.get_client_secret(),
            agent_id=configuration.get_agent_id(),
        )

packy_server_client_factory = PackyServerClientFactory()
