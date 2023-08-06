from __future__ import absolute_import


import os
import logging
from collections import defaultdict

import gevent.pool
from .gevent import async_patched


logger = logging.getLogger(__name__)


def generate_ping_arguments(ping_count, max_hops):
    unique_id = 0
    for ping_number in xrange(ping_count):
        for ttl in xrange(1, max_hops + 1):
            yield {'ttl': ttl, 'ping_number': ping_number, 'unique_id': unique_id}
            unique_id += 1


def ping(ping_function_partial, ttl, ping_number, unique_id):
    id_ = (os.getpid() + unique_id) & 0xFFFF
    try:
        return ttl, ping_number, ping_function_partial(ttl=ttl, id_=id_)
    except Exception:
        logger.exception('Error while pinging')
        return ttl, ping_number, None


def traceroute_parallel(ping_function_partial, destination_ip_address,
                        ping_count, max_hops, max_parallelism=10):
    def ping_function_partial_local(kwargs):
        return ping(ping_function_partial, **kwargs)

    destination_hop = max_hops

    results = defaultdict(dict)
    with async_patched():
        pool = gevent.pool.Pool(size=max_parallelism)
        ping_arguments = generate_ping_arguments(ping_count, max_hops)
        for ttl, ping_number, ping_result in pool.imap_unordered(ping_function_partial_local,
                                                                 ping_arguments):
            results[ttl][ping_number] = ping_result
            if ping_result:
                _, ip_address = ping_result
                if ip_address == destination_ip_address:
                    destination_hop = min(ttl, destination_hop)

    final_results = []
    for ttl in xrange(1, destination_hop + 1):
        pings = []
        final_results.append(pings)
        for ping_number in xrange(ping_count):
            pings.append(results[ttl].get(ping_number))

    return final_results
