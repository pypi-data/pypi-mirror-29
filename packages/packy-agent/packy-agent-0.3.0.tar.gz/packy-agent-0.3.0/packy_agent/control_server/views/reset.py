import logging

import flask
from flask.views import MethodView

from packy_agent.control_server.forms.action import ActionForm
from packy_agent.control_server.views.base import smart_redirect
from packy_agent.configuration.control_server.base import configuration
from packy_agent.managers.control import control_manager
from packy_agent.managers.reset import reset_manager
from packy_agent.utils.misc import is_inside_docker_container
from packy_agent.utils.auth import activation_and_authentication_required, logout


OPERATION_DELAY_SECONDS = 5

logger = logging.getLogger(__name__)


def do_action(action):
    if action == 'reset':
        if (not is_inside_docker_container() and
                not configuration.is_network_configuration_enabled()):
            flask.flash('Please, see logs for more information')

        reset_manager.reset()
        control_manager.reboot(OPERATION_DELAY_SECONDS)
    elif action == 'reset_activation':
        control_manager.stop_packy_agent()
        reset_manager.reset_agent_activation()
        logout()
    elif action == 'reset_network':
        if not configuration.is_network_configuration_enabled():
            flask.flash('Please, see logs for more information')

        reset_manager.reset_network_configuration()
        control_manager.reboot(OPERATION_DELAY_SECONDS)
    else:
        raise ValueError('Unknown action: {}'.format(action))


class ResetView(MethodView):

    @activation_and_authentication_required
    def get(self):
        form = ActionForm()
        context = {
            'form': form,
            'active_menu_item': 'reset',
        }

        return flask.render_template('reset.html', **context)

    @activation_and_authentication_required
    def post(self):
        form = ActionForm()
        if form.validate():
            action = flask.request.form['action']
            do_action(action)
            flask.flash('Operation will start in {} seconds...'.format(OPERATION_DELAY_SECONDS))
            return flask.redirect(flask.url_for('index'))

        return flask.render_template('reset.html', form=form)
