import argparse
import sys

from packy_agent.managers.network import network_manager


def set_dhcp(interface):
    network_manager.set_dhcp(interface)


def entry():
    from packy_agent.cli import generate_supervisord_conf as the_module
    parser = argparse.ArgumentParser(
        # Cannot use __name__, because when module is run as script it is equal to __main__
        prog='python -m {}'.format(the_module.__name__),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', '--interface')
    args = parser.parse_args()

    return set_dhcp(args.interface)


if __name__ == '__main__':
    sys.exit(entry())
