import flask
from flask.views import MethodView
from packy_agent.utils.auth import activation_and_authentication_required


class SuccessView(MethodView):

    @activation_and_authentication_required
    def get(self):
        context = {
            'message': 'Operation Success',
            'back_url': flask.request.args.get('back_url'),
            'button_text': flask.request.args.get('button_text', 'Back'),
        }
        return flask.render_template('success.html', **context)
