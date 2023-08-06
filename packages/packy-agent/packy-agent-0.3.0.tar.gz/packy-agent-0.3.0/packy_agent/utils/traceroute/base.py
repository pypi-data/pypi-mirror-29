from __future__ import absolute_import

import math
from functools import partial
from .icmp import ping_icmp
from .udp import ping_udp
from .parallel import traceroute_parallel
from .sequential import traceroute_sequential

import socket


ICMP_TYPE = 'icmp'
UDP_TYPE = 'udp'
TRACEROUTE_TYPES = (ICMP_TYPE, UDP_TYPE)


def aggregate_results(ping_results):
    agg_results = []
    for pings in ping_results:
        agg = {'loss': pings.count(None)}
        results = filter(None, pings)
        if results:
            agg['host'] = results[0][1]
            delays = [x[0] for x in results]
            agg['last'] = delays[-1]
            agg['best'] = min(delays)
            agg['worst'] = max(delays)
            average = sum(delays) / len(delays)
            agg['average'] = average

            variance = sum((x - average) ** 2 for x in delays) / len(delays)
            agg['stdev'] = math.sqrt(variance)
        else:
            agg['host'] = None

        agg_results.append(agg)

    return agg_results


def traceroute(host, timeout=2, ping_count=1, packet_size_bytes=64, max_hops=100, type_=ICMP_TYPE,
               max_parallelism=10):

    if max_parallelism < 1:
        raise ValueError('max_parallelism must be greater or equal to 1')

    if type_ == ICMP_TYPE:
        ping_function = ping_icmp
    elif type_ == UDP_TYPE:
        ping_function = ping_udp
        if max_parallelism > 1:
            raise NotImplementedError('Parallelism for {} traceroute is not implemented', type_)
    else:
        raise ValueError('Unknown traceroute type: {}'.format(type_))

    destination_ip_address = socket.gethostbyname(host)

    ping_function_partial = partial(ping_function, destination_ip_address, timeout=timeout,
                                    n_bytes=packet_size_bytes)
    if max_parallelism == 1:
        results = traceroute_sequential(ping_function_partial, destination_ip_address,
                                        ping_count=ping_count, max_hops=max_hops)
    else:
        results = traceroute_parallel(ping_function_partial, destination_ip_address,
                                      ping_count=ping_count, max_hops=max_hops,
                                      max_parallelism=max_parallelism)

    return aggregate_results(results)
