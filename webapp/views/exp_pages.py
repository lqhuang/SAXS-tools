from __future__ import print_function, division

import os
import glob

import yaml
from flask import render_template, Blueprint

from webapp.forms import ExperimentSetupForm

exp_pages = Blueprint(
    'exp_pages',
    __name__,
    # template_folder='templates',  # Path for templates
    # static_folder='static',  # Path for static files
)

NAME = dict()
NAME['sasimage'] = 'SAS Image'
NAME['sasprofile'] = 'SAS Profile'
NAME['cormap'] = 'Correlation Map'
NAME['difference'] = 'Sequence Analysis'
NAME['guinier'] = 'Guinier Fitting'
NAME['gnom'] = 'Pair-wise Distribution (GNOM)'
NAME['mw'] = 'Molecular Weight'

# TODO: set project root path
ROOT_PATH = 'undone'
SHOW_DASHBOARD = True


def get_exp_info(setup_file):
    try:
        with open(setup_file, 'r', encoding='utf-8') as fname:
            setup = yaml.load(fname)
    except yaml.scanner.ScannerError as err:  # syntax error: empty fields
        print(err)
        setup = {}
    return setup


@exp_pages.route('/exp_cards')
def show_exp_cards():
    setup_files = glob.glob(os.path.join(ROOT_PATH, 'EXP*/setup.yml'))
    setup_files.sort()
    exp_setup_list = [get_exp_info(filepath) for filepath in setup_files]
    return render_template('exp_cards.html', exp_setup_list=exp_setup_list)


@exp_pages.route('/exp_pages/exp<int:exp_id>')
def individual_experiment_page(exp_id):
    selected_graph = [
        'sasimage',
        'cormap',
        'sasprofile',
        'difference',
        'gnom',
    ]
    dashboard_params = [{
        'graph_type': gtype,
        'graph_name': NAME[gtype]
    } for gtype in selected_graph]

    setup_file = os.path.join(ROOT_PATH, 'EXP' + str(exp_id).zfill(2),
                              'setup.yml')
    if os.path.exists(setup_file):
        exp_setup = get_exp_info(setup_file)
    else:
        exp_setup = {}
    exp_setup_form = ExperimentSetupForm(exp_setup)

    return render_template(
        'exp_base.html',
        exp_id=exp_id,
        exp_setup_form=exp_setup_form,
        show_dashboard=SHOW_DASHBOARD,
        dashboard_params=dashboard_params)
