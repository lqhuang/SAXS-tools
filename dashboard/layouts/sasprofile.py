from __future__ import print_function, division

import os
import glob

import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from .datamodel import raw_simulator
from .style import AXIS_OPTIONS, XLABEL, YLABEL
from .style import INLINE_LABEL_STYLE, GRAPH_GLOBAL_CONFIG
from ..base import dash_app

PLOT_OPTIONS = [{
    'label': 'Profile',
    'value': 'profile',
}, {
    'label': 'Guinier',
    'value': 'guinier',
}, {
    'label': 'Kratky',
    'value': 'kratky',
}, {
    'label': 'Porod',
    'value': 'porod',
}]

layout = html.Div(children=[
    dcc.Graph(
        id='sasprofile-graph',
        figure={
            'data': [{
                'x': [1, 2, 3],
                'y': [1, 2, 3],
            }],
            'layout': {
                'height': 400,
                'hovermode': 'closest',
                'title': 'Subtracted profiles',
                'xaxis': dict(title=XLABEL['linear_q'], type='linear'),
                'yaxis': dict(title=YLABEL['linear_I'], type='linear'),
            }
        },
        config=GRAPH_GLOBAL_CONFIG,
    ),
    html.Label('Plot type'),
    dcc.RadioItems(
        id='sasprofile-plot-type',
        options=PLOT_OPTIONS,
        value='profile',
        labelStyle=INLINE_LABEL_STYLE,
    ),
    html.Label('Y axis type'),
    dcc.RadioItems(
        id='sasprofile-x-axis-scale',
        options=AXIS_OPTIONS,
        value=False,
        labelStyle=INLINE_LABEL_STYLE,
    ),
    html.Label('X axis type'),
    dcc.RadioItems(
        id='sasprofile-x-axis-scale',
        options=AXIS_OPTIONS,
        value=False,
        labelStyle=INLINE_LABEL_STYLE,
    ),
])


def get_sasprofile(exp):
    file_list = glob.glob(
        os.path.join(
            raw_simulator.get_raw_settings_value('SubtractedFilePath'),
            '*.dat'))

    sasm_list = raw_simulator.loadSASMs(file_list)

    data = [{
        'x': each_sasm.q,
        'y': each_sasm.i,
        'error_y': dict(type='data', array=each_sasm.err, visible=False),
        'type': 'line',
        'name': each_sasm.getParameter('filename')
    } for each_sasm in sasm_list]

    layout.children[0].figure['data'] = data

    return layout


# @dash_app.callback(
#     Output('sasprofile-graph', 'figure'), [
#         Input('sasprofile-x-axis-scale', 'value'),
#         Input('sasprofile-y-axis-scale', 'value'),
#         Input('sasprofile-graph', 'figure')
#     ])
# def update_x_axis_scale(xaxis_scale, yaxis_scale, figure_data):
#     figure_data.figure.layout.xaxis['title'] = XLABEL[xaxis_scale + '_q']
#     figure_data.figure.layout.xaxis['type'] = xaxis_scale
#     figure_data.figure.layout.yaxis['title'] = XLABEL[yaxis_scale + '_I']
#     figure_data.figure.layout.yaxis['type'] = yaxis_scale
#     return figure_data
