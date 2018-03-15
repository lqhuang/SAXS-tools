from __future__ import print_function, division

import os
import glob

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from .datamodel import raw_simulator
from .style import AXIS_OPTIONS, XLABEL, YLABEL
from .style import INLINE_LABEL_STYLE, GRAPH_GLOBAL_CONFIG
from ..base import dash_app

DIFF_OPTIONS = [
    {
        'label': 'Relative difference',
        'value': 'relative_diff'
    },
    {
        'label': 'Absolute difference',
        'value': 'absolute_diff'
    },
]

layout = html.Div(children=[
    dcc.Graph(
        id='difference-graph',
        figure={
            'data': [],
            'layout': {
                'height': 400,
                'hovermode': 'closest',
                'title': 'Subtracted profiles',
                'xaxis': dict(title=XLABEL['linear_q'], type='linear'),
                'yaxis': dict(title=YLABEL['relative_diff']),
            }
        },
        config=GRAPH_GLOBAL_CONFIG,
    ),
    html.Label('Select as base reference:'),
    dcc.Dropdown(
        id='difference-ref-selection',
        options=[{
            'label': 'First file',
            'value': '1'
        }, {
            'label': 'Second file',
            'value': '2'
        }, {
            'label': 'Third file',
            'value': '3'
        }],
        value='2',
    ),
    html.Label('Plot type'),
    dcc.RadioItems(
        id='difference-plot-type',
        options=DIFF_OPTIONS,
        value='relative_diff',
        labelStyle=INLINE_LABEL_STYLE,
    ),
    html.Label('X axis type'),
    dcc.RadioItems(
        id='difference-x-axis-scale',
        options=AXIS_OPTIONS,
        value=False,
        labelStyle=INLINE_LABEL_STYLE,
    ),
    html.Label('Parameters for smoothing'),
    html.Label('window length'),
    dcc.Input(
        placeholder='Enter a positive odd integer...', value=25, type=float),
    html.Label('Polyorder'),
    dcc.Input(
        placeholder='Enter an integer less than window length ...',
        value=5,
        type=float,
    ),
    # dcc.Link('Sequential difference', href='/apps/difference'),
])


def get_difference(exp):
    file_list = glob.glob(
        os.path.join(
            raw_simulator.get_raw_settings_value('SubtractedFilePath'),
            '*.dat'))
    sasm_list = raw_simulator.loadSASMs(file_list)

    ref_dat = sasm_list[0]

    data = [{
        'x': each_sasm.q,
        'y': each_sasm.i,
        'type': 'line',
        'name': each_sasm.getParameter('filename')
    } for each_sasm in sasm_list]

    layout.children[0].figure['data'] = data

    return layout


@dash_app.callback(
    Output('difference-graph', 'figure'), [
        Input('difference-x-axis-scale', 'value'),
        Input('difference-graph', 'figure')
    ])
def update_x_axis_scale(curr_x_logscale, figure_data):
    figure_data.figure.layout.xaxis['title'] = XLABEL[curr_x_logscale + '_q']
    figure_data.figure.layout.xaxis['type'] = curr_x_logscale
    return figure_data
