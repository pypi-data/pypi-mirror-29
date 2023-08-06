from collections import defaultdict


def traceroute_sequential(ping_function_partial, destination_ip_address,
                          ping_count, max_hops):
    destination_hop = max_hops
    results = defaultdict(dict)
    for ping_number in xrange(ping_count):
        for ttl in xrange(1, destination_hop + 1):
            ping_result = ping_function_partial(ttl=ttl)
            results[ttl][ping_number] = ping_result
            if ping_result:
                _, ip_address = ping_result
                if ip_address == destination_ip_address:
                    destination_hop = min(ttl, destination_hop)
                    break

    final_results = []
    for ttl in xrange(1, destination_hop + 1):
        pings = []
        final_results.append(pings)
        for ping_number in xrange(ping_count):
            pings.append(results[ttl].get(ping_number))

    return final_results