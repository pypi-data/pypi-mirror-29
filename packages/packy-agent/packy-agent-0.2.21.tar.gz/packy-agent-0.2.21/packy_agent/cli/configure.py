import argparse
import sys
import os

from packy_agent.managers.install_and_upgrade import install_and_upgrade_manager, CONFIGURE_TARGETS
from packy_agent.configuration.agent.base import configuration as agent_configuration
from packy_agent.configuration.control_server.base import configuration as cs_configuration
from packy_agent.utils.logging import KNOWN_LOG_LEVELS, configure_basic_logging
from packy_agent.utils.services.systemd import nginx_service


ACTIVATE_PACKY_AGENT_SH = """#!/usr/bin/env bash
source {venv_path}/bin/activate
packy-agent-activate
"""

def entry():
    from packy_agent.cli import configure as the_module
    parser = argparse.ArgumentParser(
        # Cannot use __name__, because when module is run as script it is equal to __main__
        prog='python -m {}'.format(the_module.__name__),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('target', choices=CONFIGURE_TARGETS)
    parser.add_argument('base_url')
    parser.add_argument('--no-restart', action='store_true')
    parser.add_argument('--remove-nginx-default-landing', action='store_true')
    parser.add_argument('--control-server-port', type=int)
    parser.add_argument('--log-level', default='INFO', choices=KNOWN_LOG_LEVELS)
    args = parser.parse_args()

    configure_basic_logging(level=args.log_level)

    control_server_port = args.control_server_port
    if control_server_port is not None:
        cs_configuration.set_control_server_port(control_server_port)

    install_and_upgrade_manager.configure(args.target, args.base_url, restart=not args.no_restart)
    if args.remove_nginx_default_landing:
        try:
            os.remove('/etc/nginx/sites-enabled/default')
        except OSError:
            pass
        nginx_service.reload()

    link = install_and_upgrade_manager.get_control_server_link(args.base_url)

    print '\n' + '-' * 40 + '\n'
    print 'Packy Agent installation (upgrade) complete'

    if not agent_configuration.is_activated():
        script_path = '/tmp/activate-packy-agent.sh'
        with open(script_path, 'w') as f:
            f.write(ACTIVATE_PACKY_AGENT_SH.format(venv_path=os.getenv('VIRTUAL_ENV')))
        os.system('chmod a+x {}'.format(script_path))

        print ('Please, activate your Packy Agent at {} or '
               'run `sudo {}`\n'.format(link, script_path))


if __name__ == '__main__':
    sys.exit(entry())
