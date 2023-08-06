import sys
import argparse
from getpass import getpass

from packy_agent.utils.logging import KNOWN_LOG_LEVELS, configure_basic_logging
from packy_agent.utils.auth import is_activated
from packy_agent.managers.install_and_upgrade import install_and_upgrade_manager
from packy_agent.exceptions import AuthenticationError, ValidationError


def entry():
    from packy_agent.cli import activate as the_module
    parser = argparse.ArgumentParser(
        # Cannot use __name__, because when module is run as script it is equal to __main__
        prog='python -m {}'.format(the_module.__name__),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--email')
    parser.add_argument('--password')
    parser.add_argument('--log-level', default='ERROR', choices=KNOWN_LOG_LEVELS)
    args = parser.parse_args()

    configure_basic_logging(level=args.log_level)

    if is_activated():
        print 'Packy Agent is already activated'
        return 1

    print 'Packy Agent activation'

    email = args.email or raw_input('E-mail: ')
    password = args.password or getpass('Password: ')

    try:
        install_and_upgrade_manager.activate(email, password, async_restart=False)
    except AuthenticationError:
        print 'Not authenticated (invalid credentials)'
        return 1
    except ValidationError as ex:
        print ex.message
        return 1

    print '\n' + '-' * 40 + '\n'
    print 'Packy Agent is activated successfully\n'


if __name__ == '__main__':
    sys.exit(entry())
