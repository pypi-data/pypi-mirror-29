from __future__ import absolute_import

import os
import struct
import socket

from packy_agent.utils.ping import (receive_one_ping, default_timer, ICMP_ECHO_REQUEST, checksum,
                                    MAX_TIME_VAL)


def send_one_ping(my_socket, dest_addr, ID, n_bytes=192):
    """
    Send one ping to the given >dest_addr<.
    """
    dest_addr = socket.gethostbyname(dest_addr)

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    my_checksum = 0
    time = default_timer()
    seq_no = int(time * 1000) & MAX_TIME_VAL # we can only store 16 bits with ms precision

    # Make a dummy header with a 0 checksum.
    header = struct.pack("bbHHH", ICMP_ECHO_REQUEST, 0, my_checksum, ID, seq_no)

    data = n_bytes * "\x00"

    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(header + data)

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack(
        "bbHHH", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, seq_no
    )
    packet = header + data
    time_sent = default_timer()
    my_socket.sendto(packet, (dest_addr, 1)) # Don't know about the 1
    return time_sent


def ping_icmp(dest_addr, timeout, n_bytes=192, ttl=0, id_=None):
    """
    Returns either the delay (in seconds) or none on timeout.
    """
    icmp = socket.getprotobyname('icmp')
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        if ttl:
            my_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    except socket.error as (errno, msg):
        if errno == 1:  # Operation not permitted
            msg = msg + (
                ' - Note that ICMP messages can only be sent from processes running as root.')
            raise socket.error(msg)
        raise

    id_ = os.getpid() & 0xFFFF if id_ is None else id_

    time_sent = send_one_ping(my_socket, dest_addr, id_, n_bytes)
    delay = receive_one_ping(my_socket, id_, timeout, time_sent=time_sent)

    my_socket.close()
    return delay