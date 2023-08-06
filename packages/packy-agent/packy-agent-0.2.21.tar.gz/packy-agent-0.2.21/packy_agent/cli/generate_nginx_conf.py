import argparse
import sys

from packy_agent.managers.install_and_upgrade import install_and_upgrade_manager


def generate_uwsgi_ini(configuration_file):
    install_and_upgrade_manager.generate_uwsgi_ini(configuration_file)


def entry():
    from packy_agent.cli import generate_uwsgi_ini as the_module
    parser = argparse.ArgumentParser(
        # Cannot use __name__, because when module is run as script it is equal to __main__
        prog='python -m {}'.format(the_module.__name__),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-c', '--configuration-file')
    args = parser.parse_args()

    pack_agent_manager.generate_nginx_conf(args.configuration_file)


if __name__ == '__main__':
    sys.exit(entry())
