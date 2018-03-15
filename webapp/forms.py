from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import Required, InputRequired


class ExperimentSetupForm(FlaskForm):
    name = StringField('Experiment ID', validators=[Required()])
    path = StringField('Experiment Path')
