from __future__ import print_function, division

import os
import glob
from typing import Union

# import yaml
from ruamel.yaml import YAML
yaml = YAML()

from flask import Blueprint
from flask import render_template, redirect, request, jsonify

from webapp.forms import (ExperimentSettingsForm, ExperimentSetupForm,
                          LayoutConfigCheckbox, SampleInfoForm)

exp_pages = Blueprint(
    'exp_pages',
    __name__,
    # template_folder='templates',  # Path for templates
    # static_folder='static',  # Path for static files
)


def to_basic_types(string: str) -> Union[bool, int, float, str]:
    if string.lower() == 'true':
        return True
    elif string.lower() == 'false':
        return False

    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except ValueError:
            return string


NAME = dict()
NAME['sasimage'] = 'SAS Image'
NAME['sasprofile'] = 'SAS Profile'
NAME['cormap'] = 'Correlation Map'
NAME['series_analysis'] = 'Series Analysis'
NAME['guinier'] = 'Guinier Fitting'
NAME['gnom'] = 'Pair-wise Distribution (GNOM)'
NAME['mw'] = 'Molecular Weight'

# TODO: set project root path
ROOT_PATH = None


def parse_yaml(yaml_file):
    try:
        with open(yaml_file, 'r', encoding='utf-8') as fstream:
            info = yaml.load(fstream)
    # except yaml.scanner.ScannerError as err:  # syntax error: empty fields
    except Exception as err:
        print(err)
        info = {}
    if info is None:
        info = {}
    return info


def dump_yaml(data, yaml_file):
    with open(yaml_file, 'w', encoding='utf-8') as fstream:
        yaml.dump(data, fstream)


@exp_pages.route('/exp_settings', methods=('GET', 'POST'))
def experiment_settings():
    exp_settings_form = ExperimentSettingsForm()
    samples_info_form = SampleInfoForm()
    return render_template(
        'exp_settings.html',
        exp_settings_form=exp_settings_form,
        samples_info_form=samples_info_form,
    )


@exp_pages.route('/exp_cards')
def show_exp_cards():
    setup_files = glob.glob(os.path.join(ROOT_PATH, 'EXP*/setup.yml'))
    setup_files.sort()
    exp_setup_list = [parse_yaml(filepath) for filepath in setup_files]
    return render_template('exp_cards.html', exp_setup_list=exp_setup_list)


@exp_pages.route('/exp_pages/exp<int:exp_id>', methods=('GET', 'POST'))
def individual_experiment_page(exp_id):

    setup_file = os.path.join(ROOT_PATH, 'EXP' + str(exp_id).zfill(2),
                              'setup.yml')
    if os.path.exists(setup_file):
        exp_setup = parse_yaml(setup_file)
    else:
        exp_setup = {}
    setup_prefix = 'setup'
    exp_setup_form = ExperimentSetupForm(exp_setup, prefix=setup_prefix)

    config_file = os.path.join(ROOT_PATH, 'EXP' + str(exp_id).zfill(2),
                               'config.yml')
    if os.path.exists(config_file):
        exp_config = parse_yaml(config_file)
        if 'layouts' not in exp_config:
            exp_config['layouts'] = []
    else:
        exp_config = {'layouts': []}
    checkbox_prefix = 'checkbox'
    layouts_checkbox = LayoutConfigCheckbox(
        exp_config['layouts'], prefix=checkbox_prefix)

    if exp_setup_form.validate_on_submit():
        for prefix_key, value in request.form.items():
            if setup_prefix:
                key = prefix_key.split('%s-' % setup_prefix)[1]
            if key not in ('csrf_token', 'submit', 'custom_params'):
                key = key.lower().replace(' ', '_')
                exp_setup[key] = to_basic_types(value)
        dump_yaml(exp_setup, setup_file)
        return redirect('/exp_pages/exp{}'.format(exp_id))

    if (layouts_checkbox.generate.data
            and layouts_checkbox.validate_on_submit()):
        curr_layouts = []
        for prefix_key in request.form.keys():
            if checkbox_prefix:
                key = prefix_key.split('%s-' % checkbox_prefix)[1]
            if key not in ('csrf_token', 'generate'):
                curr_layouts.append(key)
        exp_config['layouts'] = curr_layouts
        dump_yaml(exp_config, config_file)
        return redirect('/exp_pages/exp{}'.format(exp_id))

    if exp_config['layouts']:
        show_dashboard = True
        selected_graph = exp_config['layouts']
    else:
        show_dashboard = False
        dashboard_params = []
    if show_dashboard:
        dashboard_params = [{
            'graph_type': gtype,
            'graph_name': NAME[gtype]
        } for gtype in selected_graph if gtype != 'exp']

    return render_template(
        'exp_base.html',
        exp_id=exp_id,
        exp_setup_form=exp_setup_form,
        layouts_checkbox=layouts_checkbox,
        show_dashboard=show_dashboard,
        dashboard_params=dashboard_params)
