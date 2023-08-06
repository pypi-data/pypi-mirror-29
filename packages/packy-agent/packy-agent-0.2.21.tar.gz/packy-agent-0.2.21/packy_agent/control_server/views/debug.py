import os.path
import logging
import yaml
import pprint
import tailer

import flask
from flask.views import MethodView

from packy_agent.exceptions import ImproperlyConfigured
from packy_agent.configuration.agent.base import configuration as agent_configuration
from packy_agent.configuration.control_server.base import configuration as control_server_configuration
from packy_agent.utils.auth import activation_and_authentication_required

TAIL_SIZE = 100


logger = logging.getLogger(__name__)


def tail(filename, size=TAIL_SIZE, safe=True):
    try:
        with open(filename) as f:
            return '\n'.join(tailer.tail(f, size))
    except Exception:
        if not safe:
            raise


class DebugView(MethodView):

    @activation_and_authentication_required
    def get(self):

        logs = (
            ('Supervisor log',
             control_server_configuration.get_supervisor_log_file(),
             tail(control_server_configuration.get_supervisor_log_file())),
            ('Packy Agent stdout log',
             control_server_configuration.get_agent_stdout_log_file(),
             tail(control_server_configuration.get_agent_stdout_log_file())),
            ('Packy Agent stderr log',
             control_server_configuration.get_agent_stderr_log_file(),
             tail(control_server_configuration.get_agent_stderr_log_file())),
            ('Control Server stdout log',
             control_server_configuration.get_control_server_stdout_log_file(),
             tail(control_server_configuration.get_control_server_stdout_log_file())),
            ('Control Server stderr log',
             control_server_configuration.get_control_server_stderr_log_file(),
             tail(control_server_configuration.get_control_server_stderr_log_file())),
        )

        packy_agent_configuration_file = agent_configuration.get_local_configuration_file_path()
        if os.path.isfile(packy_agent_configuration_file):
            with open(packy_agent_configuration_file) as f:
                packy_agent_configuration_file_content = f.read()
        else:
            packy_agent_configuration_file += ' (does not exist)'
            packy_agent_configuration_file_content = ''

        packy_agent_custom_configuration = yaml.safe_dump(
            agent_configuration.get_packy_agent_configuration(), default_flow_style=False)
        try:
            packy_agent_celery_configuration = pprint.pformat(
                    agent_configuration.get_celery_configuration(), indent=4)
        except ImproperlyConfigured:
            packy_agent_celery_configuration = '(not configured)'

        control_server_configuration_file = (
            control_server_configuration.get_local_configuration_file_path())
        if os.path.isfile(control_server_configuration_file):
            with open(control_server_configuration_file) as f:
                control_server_configuration_file_content = f.read()
        else:
            control_server_configuration_file += ' (does not exist)'
            control_server_configuration_file_content = ''

        control_server_custom_configuration = yaml.safe_dump(
            control_server_configuration.get_control_server_configuration(),
            default_flow_style=False)
        control_server_flask_configuration = pprint.pformat(
            control_server_configuration.get_flask_configuration(), indent=4)

        context = {
            'packy_agent_configuration_file': packy_agent_configuration_file,
            'packy_agent_configuration_file_content': packy_agent_configuration_file_content,
            'packy_agent_custom_configuration': packy_agent_custom_configuration,
            'packy_agent_celery_configuration': packy_agent_celery_configuration,
            'control_server_configuration_file': control_server_configuration_file,
            'control_server_configuration_file_content': control_server_configuration_file_content,
            'control_server_custom_configuration': control_server_custom_configuration,
            'control_server_celery_configuration': control_server_flask_configuration,
            'logs': logs,
            'active_menu_item': 'debug',
        }

        return flask.render_template('debug.html', **context)
