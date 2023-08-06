from flask_wtf import FlaskForm
from wtforms import StringField


class ActionForm(FlaskForm):

    action = StringField('action')
