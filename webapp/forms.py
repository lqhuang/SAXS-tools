from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextAreaField
from wtforms.validators import InputRequired


class ExperimentSetupForm(FlaskForm):
    def __init__(self, setup_yaml, **form_kwargs):
        # Initial unbound_fields.
        # This will overwrite all defined fields outside of __init__().
        fields = []
        # TODO: add security filter
        for param, val in setup_yaml.items():
            if isinstance(val, str):
                gen_unbound_field = StringField
            else:
                gen_unbound_field = FloatField
            field_kwargs = dict(
                label=param.replace('_', ' ').capitalize(),
                default=val,
                validators=[InputRequired()],
            )
            fields.append((param, gen_unbound_field(**field_kwargs)))

        # TODO: add YAML syntax error checker
        extra_info_kwargs = dict(
            label='Add more extra info',
            default='example_param: parameter_value # Label name',
            description=
            'Support <a target="_blank" href="//docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html">YAML</a> syntax.',
            render_kw={"rows": 2},
        )
        fields.append(('custom_params', TextAreaField(**extra_info_kwargs)))
        fields.append(('Save', SubmitField('Save')))

        # We keep the name as the second element of the sort
        # to ensure a stable sort.
        fields.sort(key=lambda x: (x[1].creation_counter, x[0]))
        self._unbound_fields = fields

        super(ExperimentSetupForm, self).__init__(**form_kwargs)


class ProjectSettingsForm(FlaskForm):
    date = StringField('Experiment date', validators=[InputRequired()])
    participants = StringField('Participants', validators=[InputRequired()])

    root = StringField('Root path', validators=[InputRequired()])
    raw_cfg_path = StringField('RAW cfg path', validators=[InputRequired()])


class SampleListForm(FlaskForm):
    sample = StringField('Sample name')
