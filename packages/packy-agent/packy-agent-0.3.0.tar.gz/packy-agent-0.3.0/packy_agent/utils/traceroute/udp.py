from __future__ import absolute_import

import struct
import socket

from packy_agent.utils.ping import receive_one_ping, default_timer

BASE_PORT = 33434


# TODO(dmu) HIGH: It does not seem that this code ever worked. Fix it
def ping_udp(target, timeout, n_bytes, ttl):
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')

    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
    send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    timeout_struct = struct.pack('ll', timeout, 0)
    recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout_struct)

    port = BASE_PORT
    recv_socket.bind(('', port))

    time_sent = default_timer()

    # 20 for IP header and 8 for UDP header
    send_socket.sendto('\x00' * (n_bytes - 28), (target, port))

    delay = receive_one_ping(recv_socket, -1, timeout=timeout, time_sent=time_sent)
    send_socket.close()
    return delay
