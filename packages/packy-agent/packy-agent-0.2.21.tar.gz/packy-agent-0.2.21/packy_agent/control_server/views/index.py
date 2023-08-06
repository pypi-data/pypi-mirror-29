import logging

import flask
from flask.views import MethodView

from packy_agent.configuration.agent.base import configuration as agent_configuration
from packy_agent.managers.control import control_manager
from packy_agent.utils.auth import activation_and_authentication_required

logger = logging.getLogger(__name__)


class IndexView(MethodView):

    @activation_and_authentication_required
    def get(self):
        agent_id = agent_configuration.get_agent_id()
        if agent_id is None:
            logger.debug('Agent is not activated yet, redirecting to activation')
            return flask.redirect(flask.url_for('activate'))
        else:
            agent_status = control_manager.get_packy_agent_status()
            agent_status_line = agent_status[0] or 'UNKNOWN'
            if agent_status[1]:
                agent_status_line += ' (uptime {})'.format(agent_status[1])

            context = {
                'agent_status': agent_status_line,
                'active_menu_item': 'status',
            }
            return flask.render_template('index.html', **context)
