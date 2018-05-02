from __future__ import print_function, division

import os.path
import json

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from .style import XLABEL, YLABEL, TITLE, INLINE_LABEL_STYLE
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
        id='gnom-graph',
        figure={},
    ),
    html.Label('Plot type'),
    dcc.RadioItems(
        id='gnom-plot-type',
        options=_PLOT_OPTIONS,
        value='pr_distribution',
        labelStyle=INLINE_LABEL_STYLE,
    ),
    html.Label('Select gnom file to plot'),
    dcc.Dropdown(
        id='gnom-file-selection',
        options=[],
        value=0,
    ),
])

_DEFAULT_FIGURE_LAYOUT = {
    'pr_distribution': {
        'height': 500,
        'hovermode': 'closest',
        'title': TITLE['pdf'],
        'xaxis': dict(title=XLABEL['pdf']),
        'yaxis': dict(title=YLABEL['pdf']),
    },
    'fitting': {
        'height': 500,
        # 'hovermode': 'closest',
        'title': TITLE['fitting'],
        'xaxis': dict(title=XLABEL['linear']),
        'yaxis': dict(title=YLABEL['log'], type='log'),
    },
}


def get_gnom(exp):
    return _DEFAULT_LAYOUT


@dash_app.callback(
    Output('gnom-file-selection', 'options'), [Input('page-info', 'children')])
def _update_file_selection(info_json):
    exp = json.loads(info_json)['exp']
    file_list = raw_simulator.get_files(exp, 'gnom_files')
    file_basename = (os.path.basename(each) for each in file_list)
    return [{
        'label': each,
        'value': i,
    } for i, each in enumerate(file_basename)]


@dash_app.callback(
    Output('gnom-graph', 'figure'),
    [
        Input('gnom-plot-type', 'value'),
        Input('gnom-file-selection', 'value'),
    ],
    [State('page-info', 'children')],
)
def _update_figure(plot_type, iftm_index, info_json):
    exp = json.loads(info_json)['exp']
    iftm_list = raw_simulator.get_gnom(exp)

    if plot_type == 'pr_distribution':
        data = [{
            'x': each_iftm.r,
            'y': each_iftm.p,
            'type': 'line',
            'name': each_iftm.getParameter('filename')
        } for each_iftm in iftm_list]
    elif plot_type == 'fitting':
        selected_iftm = iftm_list[iftm_index]
        data = [{
            'x': selected_iftm.q_orig,
            'y': selected_iftm.i_orig,
            'type': 'line',
            'name': selected_iftm.getParameter('filename'),
        }, {
            'x': selected_iftm.q_extrap,
            'y': selected_iftm.i_extrap,
            'type': 'line',
            'name': 'fitting result',
        }]

    return {
        'data': data,
        'layout': _DEFAULT_FIGURE_LAYOUT[plot_type],
    }
