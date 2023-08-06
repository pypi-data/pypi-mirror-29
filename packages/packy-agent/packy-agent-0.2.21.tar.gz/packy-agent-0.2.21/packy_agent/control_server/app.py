import logging

import flask

import packy_agent
from packy_agent.utils.pkg_resources import get_package_file_full_path

from packy_agent.control_server.views.index import IndexView
from packy_agent.control_server.views.login import LoginView, LoginFailureView
from packy_agent.control_server.views.logout import LogoutView
from packy_agent.control_server.views.success import SuccessView
from packy_agent.control_server.views.network import NetworkView
from packy_agent.control_server.views.control import ControlView
from packy_agent.control_server.views.upgrade import UpgradeView
from packy_agent.control_server.views.reset import ResetView
from packy_agent.control_server.views.debug import DebugView
from packy_agent.control_server.views.activate import ActivateView, ActivationFailureView
from packy_agent.control_server.views import errors as error_handlers
from packy_agent.utils.misc import is_inside_docker_container

from packy_agent.configuration.control_server.base import configuration


def configure(app, packy_server_base_url=None):
    # TODO(dmu) LOW: Refactor to make autooverride from options if there are more options to
    #                override
    configuration.set_server_base_url_override(packy_server_base_url)
    configuration.get_flask_configuration()
    app.config.from_mapping(configuration.get_flask_configuration())


def setup_routes(app):
    app.add_url_rule('/', view_func=IndexView.as_view('index'))
    app.add_url_rule('/network/', view_func=NetworkView.as_view('network'))
    app.add_url_rule('/control/', view_func=ControlView.as_view('control'))
    app.add_url_rule('/upgrade/', view_func=UpgradeView.as_view('upgrade'))
    app.add_url_rule('/reset/', view_func=ResetView.as_view('reset'))
    app.add_url_rule('/debug/', view_func=DebugView.as_view('debug'))
    app.add_url_rule('/success/', view_func=SuccessView.as_view('success'))
    app.add_url_rule('/activate/', view_func=ActivateView.as_view('activate'))
    app.add_url_rule('/activation_failure/',
                     view_func=ActivationFailureView.as_view('activation_failure'))
    app.add_url_rule('/login/', view_func=LoginView.as_view('login'))
    app.add_url_rule('/login_failure/', view_func=LoginFailureView.as_view('login_failure'))
    app.add_url_rule('/logout/', view_func=LogoutView.as_view('logout'))


def setup_context_processors(app):

    @app.context_processor
    def extra_context_processor():
        return {
            'version': packy_agent.__version__,
            'is_inside_docker_container': is_inside_docker_container(),
            'is_debug_mode': configuration.is_debug_mode(),
            'configuration': configuration,
        }


def setup_error_handlers(app):
    app.register_error_handler(500, error_handlers.handle_http500)
    app.register_error_handler(401, error_handlers.handle_http401)


def get_app(packy_server_base_url=None):
    # TODO(dmu) HIGH: Improve logging configuration
    logging.basicConfig(format='%(asctime)-15s %(levelname)s [%(name)s]: %(message)s',
                        level=logging.DEBUG)

    app = flask.Flask(__name__,
                      template_folder=get_package_file_full_path(__name__, 'templates'),
                      static_folder=get_package_file_full_path(__name__, 'static'),
                      static_url_path='/assets')

    configure(app, packy_server_base_url=packy_server_base_url)
    setup_routes(app)
    setup_context_processors(app)
    setup_error_handlers(app)

    return app
