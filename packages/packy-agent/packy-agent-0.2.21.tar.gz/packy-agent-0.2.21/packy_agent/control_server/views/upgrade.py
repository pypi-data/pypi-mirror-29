import logging

import flask
from flask.views import MethodView

from packy_agent.managers.install_and_upgrade import install_and_upgrade_manager
from packy_agent.control_server.forms.action import ActionForm
from packy_agent.configuration.control_server.base import configuration
from packy_agent.control_server.views.base import smart_redirect
from packy_agent.utils.auth import activation_and_authentication_required


DELAY_SECONDS = 5

logger = logging.getLogger(__name__)


def do_action(action):
    if action == 'upgrade_and_restart':
        flask.flash('Upgrade and restart will start in {} seconds...'.format(DELAY_SECONDS))
        install_and_upgrade_manager.upgrade_and_restart(DELAY_SECONDS)
    else:
        raise ValueError('Unknown action: {}'.format(action))


class UpgradeView(MethodView):

    @activation_and_authentication_required
    def get(self):
        form = ActionForm()
        context = {
            'form': form,
            'active_menu_item': 'upgrade',
        }

        return flask.render_template('upgrade.html', **context)

    @activation_and_authentication_required
    def post(self):
        form = ActionForm()
        if form.validate():
            action = flask.request.form['action']
            do_action(action)

            if not configuration.is_upgrade_enabled():
                flask.flash('Please, see logs for more information')

            return smart_redirect('success', 'upgrade')

        return flask.render_template('upgrade.html', form=form)
