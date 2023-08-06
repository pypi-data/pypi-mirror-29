import sys
import argparse

from packy_agent.utils.traceroute import base


def do_traceroute(host, timeout=1, ping_count=1, max_hops=30, type_=base.ICMP_TYPE, max_parallelism=1):
    agg_results = base.traceroute(host, timeout=timeout, ping_count=ping_count, max_hops=max_hops,
                                  type_=type_, max_parallelism=max_parallelism)
    for x, result in enumerate(agg_results):
        print x + 1, result['host'], result


def entry():
    from packy_agent.cli import traceroute as the_module
    parser = argparse.ArgumentParser(
        # Cannot use __name__, because when module is run as script it is equal to __main__
        prog='python -m {}'.format(the_module.__name__),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('host')
    parser.add_argument('--max-hops', type=int, default=30)
    parser.add_argument('--ping-count', type=int, default=1)
    parser.add_argument('--max-parallelism', type=int, default=1)
    parser.add_argument('--timeout', type=float, default=1)
    parser.add_argument('--type', choices=base.TRACEROUTE_TYPES, default=base.ICMP_TYPE)

    args = parser.parse_args()

    return do_traceroute(args.host, timeout=args.timeout, ping_count=args.ping_count,
                         max_hops=args.max_hops, type_=args.type,
                         max_parallelism=args.max_parallelism)


if __name__ == '__main__':
    sys.exit(entry())
