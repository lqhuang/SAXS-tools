from __future__ import print_function, division

import os.path
import json

import numpy as np
from scipy.optimize import curve_fit

from plotly import tools
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from .style import XLABEL, YLABEL, TITLE, LINE_STYLE
from .style import GRAPH_GLOBAL_CONFIG
from ..base import dash_app
from ..datamodel import raw_simulator

_PLOT_OPTIONS = [{
    'label': 'P(r) distribution',
    'value': 'pr_distribution'
}, {
    'label': 'Fitting curve',
    'value': 'fitting'
}]

_DEFAULT_LAYOUT = html.Div(children=[
    dcc.Graph(
        id='guinier-graph',
        figure={},
        config=GRAPH_GLOBAL_CONFIG,
    ),
    html.Button('Auto RG (not available for now)', id='guinier-autorg'),
    html.Label('Select gnom file to plot'),
    dcc.Dropdown(
        id='guinier-file-selection',
        options=[],
        value=0,
    ),
    html.Label('Slider for q slice'),
    dcc.RangeSlider(
        id='guinier-q-range',
        # count=1,
        # disabled=True,
        min=0,
        max=100,
        step=1,
        value=[0, 20],
    ),
])


def fit_rg(sasm, qmin_idx, qmax_idx):
    rg_slice = slice(qmin_idx, qmax_idx)
    q = sasm.q
    intensity = sasm.i
    # err = sasm.err

    q_square = np.square(q)[rg_slice]
    ln_intensity = np.log(intensity)[rg_slice]

    func = lambda x, b, k: k * x + b

    opt, cov = curve_fit(func, q_square, ln_intensity)
    # print('opt:', opt)
    # print('cov:', cov)
    rg = np.sqrt(-3.0 * opt[1])
    i0 = np.exp(opt[0])

    rg_err = np.absolute(0.5 * (
        np.sqrt(-3.0 / opt[1]))) * np.sqrt(np.absolute(cov[1, 1]))
    i0_err = i0 * np.sqrt(np.absolute(cov[0, 0]))
    # FIXME: rg_err and i0_err are probably not correct!

    qRg_min = q[qmin_idx] * rg
    qRg_max = q[qmax_idx] * rg

    return rg, rg_err, i0, i0_err, qRg_min, qRg_max


def get_guinier(exp):
    return _DEFAULT_LAYOUT


@dash_app.callback(
    Output('guinier-file-selection', 'options'),
    [Input('page-info', 'children')])
def _update_file_selection(info_json):
    exp = json.loads(info_json)['exp']
    file_list = raw_simulator.get_files(exp, 'subtracted_files')
    file_basename = (os.path.basename(each) for each in file_list)
    if file_list:
        return [{
            'label': each,
            'value': i,
        } for i, each in enumerate(file_basename)]
    else:
        return [{
            'label': 'No files found.',
            'value': 0,
        }]


@dash_app.callback(
    Output('guinier-graph', 'figure'),
    [
        Input('guinier-file-selection', 'value'),
        Input('guinier-q-range', 'value'),
    ],
    [State('page-info', 'children')],
)
def _update_figure(sasm_idx, q_range, info_json):

    exp = json.loads(info_json)['exp']
    sasm = raw_simulator.get_sasprofile(exp)[sasm_idx]
    rg, _, i0, _, qRg_min, qRg_max = fit_rg(sasm, *q_range)

    q = sasm.q
    intensity = sasm.i
    rg_slice = slice(*q_range)
    fitting_curve = np.log(i0) - rg**2.0 / 3.0 * q[rg_slice]**2.0

    figure = tools.make_subplots(rows=2, cols=1, print_grid=False)
    # first subplot
    figure['data'] += [
        {
            'x': q[rg_slice],
            'y': np.log(intensity[rg_slice]),  # ln scale
            'mode': 'markers',
            # 'line': dict(dash='dot', **LINE_STYLE),
            'name': 'source curve',
        },
        {
            'x': q[rg_slice],
            'y': fitting_curve,
            'line': LINE_STYLE,
            'name': 'fitting curve',
        }
    ]
    # second subplot
    figure['data'] += [{
        'x': q[rg_slice],
        'y': intensity[rg_slice] - np.exp(fitting_curve),
        'mode': 'markers',
        # 'line': dict(dash='dot', **LINE_STYLE),
        'name': 'residual',
        'xaxis': 'x2',
        'yaxis': 'y2',
    }, {
        'x': q[rg_slice],
        'y': np.zeros_like(q[rg_slice]),
        'line': LINE_STYLE,
        'name': 'zero',
        'xaxis': 'x2',
        'yaxis': 'y2',
    }]  # yapf: disable

    rg_res = 'Rg={:.4f}, I0={:.4f}, curr index(qRg limits): ({}, {})({:.4f}, {:.4f})'.format(
        rg, i0, q_range[0], q_range[1], qRg_min, qRg_max)
    figure['layout'].update(dict(title=rg_res, height=500))
    figure['layout']['xaxis2'].update({'title': XLABEL['guinier']})
    figure['layout']['yaxis1'].update({'title': YLABEL['guinier']})
    figure['layout']['yaxis2'].update({'title': 'Residual'})

    return figure
