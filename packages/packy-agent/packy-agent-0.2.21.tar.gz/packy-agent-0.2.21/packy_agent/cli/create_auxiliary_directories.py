import argparse
import sys

from packy_agent.managers.install_and_upgrade import install_and_upgrade_manager


def create_auxiliary_directories():
    install_and_upgrade_manager.create_auxiliary_directories()


def entry():
    from packy_agent.cli import generate_supervisord_conf as the_module
    parser = argparse.ArgumentParser(
        # Cannot use __name__, because when module is run as script it is equal to __main__
        prog='python -m {}'.format(the_module.__name__),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_args()

    return create_auxiliary_directories()


if __name__ == '__main__':
    sys.exit(entry())
