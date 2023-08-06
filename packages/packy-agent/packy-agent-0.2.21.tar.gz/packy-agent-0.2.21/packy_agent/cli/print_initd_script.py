import argparse
import sys

from packy_agent.managers.install_and_upgrade import install_and_upgrade_manager


def get_packy_initd_script_content(operating_system):
    print install_and_upgrade_manager.get_packy_initd_script_content(operating_system)


def entry():
    from packy_agent.cli import generate_supervisord_conf as the_module
    parser = argparse.ArgumentParser(
        # Cannot use __name__, because when module is run as script it is equal to __main__
        prog='python -m {}'.format(the_module.__name__),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('operating_system')
    args = parser.parse_args()

    return get_packy_initd_script_content(operating_system=args.operating_system)


if __name__ == '__main__':
    sys.exit(entry())
