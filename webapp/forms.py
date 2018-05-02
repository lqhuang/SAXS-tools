from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, FloatField, TextAreaField,
                     SubmitField)
from wtforms.validators import InputRequired


class ExperimentSetupForm(FlaskForm):
    def __init__(self, setup_yaml, **form_kwargs):
        # Initial unbound_fields.
        # This will overwrite all defined fields outside of __init__().
        fields = []
        # TODO: add security filter
        for param, val in setup_yaml.items():
            if isinstance(val, float):
                gen_unbound_field = FloatField
            else:
                gen_unbound_field = StringField
            field_kwargs = dict(
                label=param.replace('_', ' ').capitalize(),
                default=val,
                validators=[InputRequired()],
            )
            fields.append((param, gen_unbound_field(**field_kwargs)))

        # TODO: add YAML syntax error checker
        extra_info_kwargs = dict(
            label='Add more extra info',
            description=
            'Support <a target="_blank" href="//docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html">YAML</a> syntax.',
            render_kw={
                'rows': 2,
                'placeholder': 'example_param: parameter_value # Label name',
            },
        )
        fields.append(('custom_params', TextAreaField(**extra_info_kwargs)))
        fields.append(('save', SubmitField('Save')))

        # We keep the name as the second element of the sort
        # to ensure a stable sort.
        fields.sort(key=lambda x: (x[1].creation_counter, x[0]))
        self._unbound_fields = fields

        super(ExperimentSetupForm, self).__init__(**form_kwargs)


class LayoutConfigCheckbox(FlaskForm):
    layout_options = [
        ('sasimage', 'SAS Images'),
        ('cormap', 'CorMap Analysis'),
        ('sasprofile', 'SAS Profile'),
        ('series_analysis', 'Series Analysis'),
        ('guinier', 'Guinier'),
        ('gnom', 'GNOM'),
    ]

    def __init__(self, layouts, **form_kwargs):
        """[summary]

        Parameters
        ----------
        layouts : iterable object
            collection of layouts
        """
        layouts_dict = {key: True for key in layouts}
        fields = []
        for name, label in self.layout_options:
            field_kwargs = dict(
                label=label, default=layouts_dict.get(name, False))
            fields.append((name, BooleanField(**field_kwargs)))

        fields.append(('generate', SubmitField('Generate')))

        # We keep the name as the second element of the sort
        # to ensure a stable sort.
        fields.sort(key=lambda x: (x[1].creation_counter, x[0]))
        self._unbound_fields = fields
        super(LayoutConfigCheckbox, self).__init__(**form_kwargs)


class ExperimentSettingsForm(FlaskForm):
    date = StringField('Experiment date', validators=[InputRequired()])
    participants = StringField('Participants', validators=[InputRequired()])

    root = StringField('Root path', validators=[InputRequired()])
    raw_cfg_path = StringField('RAW cfg path', validators=[InputRequired()])

    default_setup_params = TextAreaField(
        'Default setup parameters',
        render_kw={
            'rows':
            1,
            'placeholder':
            'example: sample, concentration, ... (separate by comma)'
        })

    save = SubmitField(label='Save')


class SampleInfoForm(FlaskForm):
    samples = TextAreaField(
        label='Add more samples information',
        description=
        'Support <a target="_blank" href="//docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html">YAML</a> syntax.',
        render_kw={
            'rows': 4,
            'placeholder': 'sample_name: concentration # mg/ml',
        },
    )
    save = SubmitField(label='Save')
