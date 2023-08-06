import argparse
import sys

from packy_agent.managers.install_and_upgrade import install_and_upgrade_manager


def generate_uwsgi_ini(configuration_file, is_development=False):
    install_and_upgrade_manager.generate_uwsgi_ini(configuration_file,
                                                   is_development=is_development)


def entry():
    from packy_agent.cli import generate_uwsgi_ini as the_module
    parser = argparse.ArgumentParser(
        # Cannot use __name__, because when module is run as script it is equal to __main__
        prog='python -m {}'.format(the_module.__name__),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--configuration-file')
    parser.add_argument('-d', '--development', action='store_true')
    args = parser.parse_args()

    return generate_uwsgi_ini(configuration_file=args.configuration_file,
                              is_development=args.development)


if __name__ == '__main__':
    sys.exit(entry())
