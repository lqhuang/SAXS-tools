from __future__ import print_function, division

import os
import json

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from .style import XLABEL, YLABEL, TITLE, LINE_STYLE
from .style import AXIS_OPTIONS
from .style import INLINE_LABEL_STYLE, GRAPH_GLOBAL_CONFIG
from ..base import dash_app
from ..datamodel import raw_simulator

_DIFF_OPTIONS = [{
    'label': 'Relative difference',
    'value': 'relative_diff',
}, {
    'label': 'Absolute difference',
    'value': 'absolute_diff',
}, {
    'label': 'Error',
    'value': 'error',
}, {
    'label': 'Error relative difference',
    'value': 'error_relative_diff',
}]

_CALC_FUNCTION = {
    'relative_diff': lambda x, ref: (x.i - ref.i) / ref.i * 100.0,
    'absolute_diff': lambda x, ref: x.i - ref.i,
    'error': lambda x, ref: x.err,
    'error_relative_diff': lambda x, ref: (x.err - ref.err) / ref.err * 100.0,
}

_DEFAULT_PLOT_TYPE = 'relative_diff'

_DEFAULT_LAYOUT = html.Div(children=[
    dcc.Graph(
        id='difference-graph',
        figure={},
        config=GRAPH_GLOBAL_CONFIG,
    ),
    html.Label('Select as base reference:'),
    dcc.Dropdown(
        id='difference-ref-selection',
        options={},
        value=0,
    ),
    html.Label('Plot type'),
    dcc.RadioItems(
        id='difference-plot-type',
        options=_DIFF_OPTIONS,
        value=_DEFAULT_PLOT_TYPE,
        labelStyle=INLINE_LABEL_STYLE,
    ),
    html.Label('X axis type'),
    dcc.RadioItems(
        id='difference-xaxis-scale',
        options=AXIS_OPTIONS,
        value='linear',
        labelStyle=INLINE_LABEL_STYLE,
    ),
    html.Label('Slider for xlim'),
    dcc.RangeSlider(
        id='difference-xlim',
        # count=1,
        # disabled=True,
        min=0.0,
        max=0.20,
        step=0.01,
        value=[0.0, 0.14],
    ),
    html.Label('Slider for ylim'),
    dcc.RangeSlider(
        id='difference-ylim',
        min=-150.0,
        max=150.0,
        step=1.0,
        value=[-50.0, 50.0],
    ),
    # html.Label('Parameters for smoothing'),
    # html.Label('window length'),
    # dcc.Input(
    #     placeholder='Enter a positive odd integer...', value=25,
    #     type='number'),
    # html.Label('Polyorder'),
    # dcc.Input(
    #     placeholder='Enter an integer less than window length ...',
    #     value=5,
    #     type='number',
    # ),
])


def get_series_analysis(exp):
    return _DEFAULT_LAYOUT


def _get_figure(exp, plot_type, ref_idx, xaxis_scale, xlim=None, ylim=None):

    sasm_list = raw_simulator.get_sasprofile(exp)
    if 'diff' in plot_type.lower():
        ref_sasm = sasm_list[ref_idx]
    else:
        ref_sasm = None

    xaxis = dict(title=XLABEL[xaxis_scale], type=xaxis_scale)
    yaxis = dict(title=YLABEL[plot_type])
    if xlim:
        xaxis['range'] = xlim
    if ylim:
        yaxis['range'] = ylim

    data = [{
        'x': each_sasm.q,
        'y': _CALC_FUNCTION[plot_type](each_sasm, ref_sasm),
        'type': 'line',
        'line': LINE_STYLE,
        'name': each_sasm.getParameter('filename'),
    } for each_sasm in sasm_list]

    return {
        'data': data,
        'layout': {
            'height': 500,
            'hovermode': 'closest',
            'title': TITLE[plot_type],
            'xaxis': xaxis,
            'yaxis': yaxis,
        },
    }


@dash_app.callback(
    Output('difference-graph', 'figure'),
    [
        Input('difference-plot-type', 'value'),
        Input('difference-ref-selection', 'value'),
        Input('difference-xaxis-scale', 'value'),
        Input('difference-xlim', 'value'),
        Input('difference-ylim', 'value'),
    ],
    [State('page-info', 'children')],
)
def _update_figure(plot_type, ref_idx, xaxis_scale, xlim, ylim, info_json):
    info_dict = json.loads(info_json)
    exp = info_dict['exp']
    return _get_figure(exp, plot_type, ref_idx, xaxis_scale, xlim, ylim)


@dash_app.callback(
    Output('difference-ref-selection', 'options'),
    [Input('page-info', 'children')])
def _set_ref_options(info_json):
    exp = json.loads(info_json)['exp']
    file_list = raw_simulator.get_files(exp, 'subtracted_files')
    return [{
        'label': os.path.basename(each),
        'value': i,
    } for i, each in enumerate(file_list)]
