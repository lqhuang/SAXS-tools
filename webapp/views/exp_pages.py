from __future__ import print_function, division

import os
import glob
from typing import Union
from collections import Iterable
import zipfile

# import yaml
from ruamel.yaml import YAML
yaml = YAML()

from flask import Blueprint
from flask import render_template, redirect, request, jsonify
from flask import send_from_directory, send_file

from webapp.forms import (ExperimentSettingsForm, ExperimentSetupForm,
                          LayoutConfigCheckbox, SampleInfoForm)

from dashboard.datamodel import raw_simulator

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

DOWNLOADABLE = {
    'sasprofile': True,
    'gnom': True,
}

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


@exp_pages.route('/exp_settings/', methods=('GET', 'POST'))
def experiment_settings():
    exp_settings_form = ExperimentSettingsForm()
    samples_info_form = SampleInfoForm()
    return render_template(
        'exp_settings.html',
        exp_settings_form=exp_settings_form,
        samples_info_form=samples_info_form,
    )


@exp_pages.route('/exp_pages/')
@exp_pages.route('/exp_cards/')
def show_exp_cards():
    if isinstance(ROOT_PATH, str):
        setup_files = glob.glob(os.path.join(ROOT_PATH, '*', 'setup.yml'))
    elif isinstance(ROOT_PATH, Iterable):
        setup_files = sum(
            [glob.glob(os.path.join(r, '*', 'setup.yml')) for r in ROOT_PATH],
            [])
    setup_files.sort()

    exp_name_list = [
        os.path.basename(os.path.dirname(filepath)) for filepath in setup_files
    ]
    exp_setup_list = [parse_yaml(filepath) for filepath in setup_files]
    return render_template(
        'exp_cards.html',
        exp_table_list=enumerate(zip(exp_name_list, exp_setup_list)),
    )


@exp_pages.route('/exp_pages/<string:exp_name>/', methods=('GET', 'POST'))
def individual_experiment_page(exp_name: str):
    exp_dir_glob = glob.glob(os.path.join(ROOT_PATH, exp_name))
    if not exp_dir_glob:
        return 'Ops. No pattern found.'
    elif len(exp_dir_glob) > 1:
        return 'Warning. There exist one more directories with the same name.'
    else:
        exp_dir_path = exp_dir_glob[0]

    setup_file = os.path.join(exp_dir_path, 'setup.yml')
    if os.path.exists(setup_file):
        exp_setup = parse_yaml(setup_file)
    else:
        exp_setup = {}
    setup_prefix = 'setup'
    exp_setup_form = ExperimentSetupForm(exp_setup, prefix=setup_prefix)

    config_file = os.path.join(exp_dir_path, 'config.yml')
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
        return redirect('/exp_pages/{}'.format(exp_name))

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
        raw_simulator.reset_exp(exp_name)
        return redirect('/exp_pages/{}'.format(exp_name))

    if exp_config['layouts']:
        show_dashboard = True
        selected_graph = exp_config['layouts']
    else:
        show_dashboard = False
        dashboard_params = []
    if show_dashboard:
        dashboard_params = [{
            'graph_type': gtype,
            'graph_name': NAME[gtype],
            'downloadable': DOWNLOADABLE.get(gtype, False),
        } for gtype in selected_graph if gtype != 'exp']

    exp_id = int(exp_name[3:])
    prev_exp_name = 'EXP%s' % str(exp_id - 1).zfill(2)
    next_exp_name = 'EXP%s' % str(exp_id + 1).zfill(2)

    return render_template(
        'exp_base.html',
        exp_id=exp_id,
        exp_name=exp_name,
        exp_setup_form=exp_setup_form,
        layouts_checkbox=layouts_checkbox,
        show_dashboard=show_dashboard,
        dashboard_params=dashboard_params,
        next_exp_name=next_exp_name,
        prev_exp_name=prev_exp_name,
    )


SUBFOLDER = {
    'sasprofile': 'Subtracted',
    'gnom': 'GNOM',
}


@exp_pages.route(
    '/download_files/<string:graph_type>/<string:exp_name>/', methods=['GET'])
def download_files(graph_type, exp_name):
    directory = os.path.join(ROOT_PATH, exp_name)
    filename = os.path.join(directory, '%s_%s.zip' % (exp_name, graph_type))
    if zipfile.is_zipfile(filename):
        return send_file(filename, as_attachment=True)
    else:
        # try to create zip file.
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except PermissionError:
                return ('Ops! PermissionError:'
                        'Failed to remove pre-exist files.')
        sub_dir = os.path.join(directory, SUBFOLDER[graph_type])
        all_files = os.listdir(sub_dir)
        if all_files:  # not empty
            all_files_path = (os.path.join(sub_dir, each)
                              for each in all_files)
            try:
                with zipfile.ZipFile(filename, 'w',
                                     zipfile.ZIP_DEFLATED) as myzip:
                    # TODO: improve encoding problem with non-latin characters
                    # Note: There is no official file name encoding for ZIP files.
                    # If you have unicode file names, you must convert them to
                    # byte strings in your desired encoding before passing them
                    # to `write()`. WinZip interprets all file names as encoded
                    # in CP437, also known as DOS Latin.
                    for fp in all_files_path:
                        myzip.write(fp, os.path.relpath(fp, directory))
            except FileExistsError:
                return 'File exists.'
            except Exception as err:
                return str(err)
            return send_file(filename, as_attachment=True)
        else:
            return 'Ops! No files found.'
