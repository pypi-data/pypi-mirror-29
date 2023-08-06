from __future__ import absolute_import

import socket
import warnings

from urlparse import urlparse


def get_machine_ip_address(host_to_reach='10.255.255.255'):
    # As suggested here:
    # https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib

    # TODO(dmu) HIGH: Support multiple interfaces properly (how is it?)
    socket_obj = None
    try:
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # to report the interface that is actually used for connection to Packy Server
            socket_obj.connect((host_to_reach, 1))
        except Exception:
            # destination does not have to be reachable
            socket_obj.connect(('10.255.255.255', 1))
        return socket_obj.getsockname()[0]
    except Exception:
        warnings.warn('Could not get actual IP address')
        return
    finally:
        if socket_obj:
            socket_obj.close()


def get_hostname_from_url(url):
    return urlparse(url).netloc.split(':')[0]
