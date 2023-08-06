import uuid
import logging

import flask
from flask.views import MethodView

from packy_agent.clients.packy_server import PackyServerClient
from packy_agent.control_server.forms.login import LoginForm
from packy_agent.configuration.control_server.base import (
    configuration as control_server_configuration)
from packy_agent.configuration.agent.base import configuration as agent_configuration

from packy_agent.utils.auth import set_authentication_cookie, activation_required


logger = logging.getLogger(__name__)


class LoginView(MethodView):

    @activation_required
    def get(self):
        return flask.render_template('login.html', form=LoginForm())

    @activation_required
    def post(self):
        form = LoginForm()
        if form.validate():
            # TODO(dmu) HIGH: Simplify this. Just get final config in one request
            client = PackyServerClient(
                base_url=control_server_configuration.get_server_base_url())

            if not client.validate_auth(form.email.data, form.password.data,
                                        agent_configuration.get_agent_id()):
                flask.flash('Not authenticated (invalid credentials)')
                return flask.redirect(flask.url_for('login_failure'))

            set_authentication_cookie()
            url = flask.request.args.get('next')
            if not url:
                url = flask.url_for('index')

            return flask.redirect(url)

        return flask.render_template('login.html', form=form)


class LoginFailureView(MethodView):

    def get(self):
        return flask.render_template('login_failure.html')
