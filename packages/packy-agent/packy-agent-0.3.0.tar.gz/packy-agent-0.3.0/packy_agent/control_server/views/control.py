import logging

import flask
from flask.views import MethodView

from packy_agent.managers.control import control_manager
from packy_agent.control_server.forms.action import ActionForm
from packy_agent.control_server.views.base import smart_redirect
from packy_agent.utils.auth import activation_and_authentication_required


DELAY_SECONDS = 5

logger = logging.getLogger(__name__)


def do_action(action):
    if action == 'reboot':
        flask.flash('Reboot will start in {} seconds...'.format(DELAY_SECONDS))
        control_manager.reboot(delay_seconds=DELAY_SECONDS)
    elif action == 'start_agent':
        control_manager.start_packy_agent()
    elif action == 'stop_agent':
        control_manager.stop_packy_agent()
    elif action == 'restart_agent':
        control_manager.restart_packy_agent()
    elif action == 'restart':
        # Restart is delayed because we need to send HTTP response before Control Server goes down
        flask.flash('Restart will start in {} seconds...'.format(DELAY_SECONDS))
        control_manager.restart(delay_seconds=DELAY_SECONDS)
    elif action == 'restart_control_server':
        # Restart is delayed because we need to send HTTP response before Control Server goes down
        flask.flash('Restart will start in {} seconds...'.format(DELAY_SECONDS))
        control_manager.restart_control_server(delay_seconds=DELAY_SECONDS)
    else:
        raise ValueError('Unknown action: {}'.format(action))


class ControlView(MethodView):

    @activation_and_authentication_required
    def get(self):
        form = ActionForm()

        agent_status = control_manager.get_packy_agent_status()
        agent_status_line = agent_status[0] or 'UNKNOWN'
        if agent_status[1]:
            agent_status_line += ' (uptime {})'.format(agent_status[1])

        context = {
            'form': form,
            'agent_status': agent_status_line,
            'active_menu_item': 'control',
        }

        return flask.render_template('control.html', **context)

    @activation_and_authentication_required
    def post(self):
        form = ActionForm()
        if form.validate():
            action = flask.request.form['action']
            do_action(action)
            return smart_redirect('success', 'control')

        return flask.render_template('control.html', form=form)
