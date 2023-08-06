import sys
import argparse

from packy_agent.managers.control import control_manager


def restart():
    control_manager.restart()


def entry():
    from packy_agent.cli import generate_uwsgi_ini as the_module
    parser = argparse.ArgumentParser(
        # Cannot use __name__, because when module is run as script it is equal to __main__
        prog='python -m {}'.format(the_module.__name__),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    args = parser.parse_args()

    return restart()


if __name__ == '__main__':
    sys.exit(entry())