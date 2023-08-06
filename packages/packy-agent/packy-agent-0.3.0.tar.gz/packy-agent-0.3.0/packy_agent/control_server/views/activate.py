import logging

import flask
from flask.views import MethodView

from packy_agent.control_server.forms.activate import ActivateForm
from packy_agent.control_server.views.base import smart_redirect
from packy_agent.exceptions import AuthenticationError, ValidationError
from packy_agent.utils.auth import set_authentication_cookie, is_activated
from packy_agent.managers.install_and_upgrade import install_and_upgrade_manager


logger = logging.getLogger(__name__)


class ActivateView(MethodView):

    def get(self):
        if is_activated():
            return flask.redirect(flask.url_for('index'))

        return flask.render_template('activate.html', form=ActivateForm())

    def post(self):
        if is_activated():
            return flask.redirect(flask.url_for('index'))

        form = ActivateForm()
        if form.validate():
            email = form.email.data
            password = form.password.data

            try:
                install_and_upgrade_manager.activate(email, password)
            except AuthenticationError:
                flask.flash('Not authenticated (invalid credentials)')
                return flask.redirect(flask.url_for('activation_failure'))
            except ValidationError as ex:
                flask.flash(ex.message)
                return flask.redirect(flask.url_for('activation_failure'))
            except Exception:
                logger.exception('Error during activation')
                flask.flash('Error during activation')
                return flask.redirect(flask.url_for('activation_failure'))

            set_authentication_cookie()
            return smart_redirect('success', 'index', button_text='Continue')

        return flask.render_template('activate.html', form=form)


class ActivationFailureView(MethodView):

    def get(self):
        return flask.render_template('activation_failure.html')
