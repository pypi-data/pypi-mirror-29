import logging

import flask
from flask.views import MethodView
from packy_agent.utils.auth import logout


logger = logging.getLogger(__name__)


class LogoutView(MethodView):

    def post(self):
        logout()
        return flask.redirect(flask.url_for('login'))
