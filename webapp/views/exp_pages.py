from __future__ import print_function, division

import os
import glob

import yaml
from flask import render_template, Blueprint

exp_pages = Blueprint(
    'exp_pages',
    __name__,
    # template_folder='templates',  # Path for templates
    # static_folder='static',  # Path for static files
)

NAME = dict()
NAME['sasimage'] = 'SAS image'
NAME['sasprofile'] = 'SAS profile'
NAME['cormap'] = 'Correlation map'
NAME['difference'] = 'Sequence'
NAME['guinier'] = 'Guinier fitting'
NAME['gnom'] = 'Pair-wise distribution (GNOM)'
NAME['mw'] = 'Molecular weight'

# TODO: set project root path
ROOT_PATH = 'undone'


def get_exp_info(setup_file):
    with open(setup_file, 'r') as fname:
        setup = yaml.load(fname)
    return setup


@exp_pages.route('/exp_cards')
def show_exp_cards():
    setup_files = glob.glob(os.path.join(ROOT_PATH, 'EXP*/setup.yml'))
    setup_files.sort()
    exp_setup_list = [get_exp_info(filepath) for filepath in setup_files]
    return render_template('exp_cards.html', exp_setup_list=exp_setup_list)


@exp_pages.route('/exp_pages/exp<exp_id>')
def individual_experiment_page(exp_id):
    selected_graph = ['sasimage', 'sasprofile', 'cormap', 'difference', 'gnom']
    dashboard_params = [{
        'graph_type': gtype,
        'graph_name': NAME[gtype]
    } for gtype in selected_graph]

    setup_file = os.path.join(ROOT_PATH, 'EXP' + str(exp_id).zfill(2),
                              'setup.yml')
    if os.path.exists(setup_file):
        exp_setup = get_exp_info(setup_file)
    else:
        exp_setup = {'None': 'Missing setup file'}
    return render_template(
        'exp_base.html',
        exp_id=exp_id,
        exp_setup=exp_setup,
        dashboard_params=dashboard_params)
