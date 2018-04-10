from __future__ import print_function, division

import os
import glob

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from .datamodel import raw_simulator
from .style import XLABEL, YLABEL, TITLE
from .style import AXIS_OPTIONS
from .style import INLINE_LABEL_STYLE, GRAPH_GLOBAL_CONFIG
from ..base import dash_app

_DIFF_OPTIONS = [{
    'label': 'Relative difference',
    'value': 'relative_diff',
}, {
    'label': 'Absolute difference',
    'value': 'absolute_diff',
}]


def _get_default_layout(exp):
    file_list = glob.glob(
        os.path.join(
            raw_simulator.get_raw_settings_value('SubtractedFilePath'),
            '*.dat'))
    file_list.sort()
    ref_options = [{
        'label': os.path.basename(each),
        'value': i,
    } for i, each in enumerate(file_list)]

    default_plot_type = 'relative_diff'

    layout = html.Div(children=[
        dcc.Graph(
            id='difference-graph',
            figure=_get_figure(default_plot_type, 0, 'linear'),
            config=GRAPH_GLOBAL_CONFIG,
        ),
        html.Label('Select as base reference:'),
        dcc.Dropdown(
            id='difference-ref-selection',
            options=ref_options,
            value=0,
        ),
        html.Label('Plot type'),
        dcc.RadioItems(
            id='difference-plot-type',
            options=_DIFF_OPTIONS,
            value=default_plot_type,
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
            value=[0.0, 0.20],
        ),
        html.Label('Parameters for smoothing'),
        html.Label('window length'),
        dcc.Input(
            placeholder='Enter a positive odd integer...',
            value=25,
            type='number'),
        html.Label('Polyorder'),
        dcc.Input(
            placeholder='Enter an integer less than window length ...',
            value=5,
            type='number',
        ),
    ])
    return layout


def _get_figure(plot_type, ref_idx, xaxis_scale, xlim=None):
    file_list = glob.glob(
        os.path.join(
            raw_simulator.get_raw_settings_value('SubtractedFilePath'),
            '*.dat'))
    sasm_list = raw_simulator.loadSASMs(file_list)

    ref_dat = sasm_list[0]

    xaxis = dict(title=XLABEL[xaxis_scale], type=xaxis_scale)
    yaxis = dict(title=YLABEL[plot_type])
    if xlim:
        xaxis['range'] = xlim

    data = [{
        'x': each_sasm.q,
        'y': each_sasm.i,
        'type': 'line',
        'name': each_sasm.getParameter('filename'),
    } for each_sasm in sasm_list]

    figure = {
        'data': data,
        'layout': {
            'height': 400,
            'hovermode': 'closest',
            'title': TITLE[plot_type],
            'xaxis': xaxis,
            'yaxis': yaxis,
        },
    }
    return figure


def get_difference(exp):
    return _get_default_layout(exp)


@dash_app.callback(
    Output('difference-graph', 'figure'), [
        Input('difference-plot-type', 'value'),
        Input('difference-ref-selection', 'value'),
        Input('difference-xaxis-scale', 'value'),
        Input('difference-xlim', 'value'),
    ])
def _update_x_axis_scale(plot_type, ref_idx, xaxis_scale, xlim):
    return _get_figure(plot_type, ref_idx, xaxis_scale, xlim)
