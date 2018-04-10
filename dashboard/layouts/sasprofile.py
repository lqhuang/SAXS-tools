from __future__ import print_function, division

import os
import glob

import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Th, Tr, Td
from dash.dependencies import Input, Output, State

from .datamodel import raw_simulator
from .style import XLABEL, YLABEL, TITLE
from .style import ERRORBAR_OPTIONS
from .style import INLINE_LABEL_STYLE, GRAPH_GLOBAL_CONFIG
from ..base import dash_app

_LIN_LIN = ('linear', 'linear')
_LOG_LIN = ('log', 'linear')
_LOG_LOG = ('log', 'log')
_LIN_LOG = ('linear', 'log')

_PLOT_OPTIONS = [{
    'label': 'Linear-Linear',
    'value': _LIN_LIN,
}, {
    'label': 'Log-Linear',
    'value': _LOG_LIN,
}, {
    'label': 'Log-Log',
    'value': _LOG_LOG,
}, {
    'label': 'Linear-Log',
    'value': _LIN_LOG,
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


def get_sasprofile(exp):
    return _get_default_layout(exp)


def _get_default_layout(exp):
    line_table = html.Table(children=[
        html.Thead([
            Th('Curves'),
            Th('Marker'),
            Th('Linestyle'),
            Th('Removed'),
        ]),
        Tr([
            Td('1'),
            Td('2'),
            Td('3'),
            Td('4'),
        ]),
        Tr([
            Td('5'),
            Td('6'),
            Td('7'),
            Td('8'),
        ]),
    ])

    default_plot_type = _LOG_LIN
    layout = html.Div(children=[
        dcc.Graph(
            id='sasprofile-graph',
            figure=_get_figure(default_plot_type, False),
            config=GRAPH_GLOBAL_CONFIG,
        ),
        html.Details(children=[
            html.Summary('Label of the item'),
            html.Div(children=line_table),
        ]),
        html.Label('Plot type'),
        dcc.RadioItems(
            id='sasprofile-plot-type',
            options=_PLOT_OPTIONS,
            value=default_plot_type,
            labelStyle=INLINE_LABEL_STYLE,
        ),
        html.Label('Show error bar'),
        dcc.RadioItems(
            id='sasprofile-errorbar',
            options=ERRORBAR_OPTIONS,
            value=False,
            labelStyle=INLINE_LABEL_STYLE,
        ),
        # html.Label('Set xlim'),
        # dcc.Input(
        #     id='sasprofile-xlim',
        #     placeholder='Enter a xlim...',
        #     # inputmode='numeric',
        #     type='text',
        #     value='0.20',
        # ),
        html.Label('Slider for xlim'),
        dcc.RangeSlider(
            id='sasprofile-xlim',
            # count=1,
            # disabled=True,
            min=0.0,
            max=0.20,
            step=0.01,
            value=[0.0, 0.20],
        ),
    ])
    return layout


def _get_figure(plot_type, errorbar_visible, xlim=None):
    profile_name = plot_type if isinstance(plot_type, str) else 'sasprofile'
    if profile_name == 'sasprofile':
        ylabel, xlabel = plot_type  # tuple
    else:
        ylabel, xlabel = 'linear', 'linear'
        errorbar_visible = False
    xaxis = dict(
        id='sasprofile-xaxis',
        title=XLABEL[xlabel],
        type=xlabel,
        # range=[0.0, xlim],
    )
    yaxis = dict(
        title=YLABEL[ylabel],
        type=ylabel,
        # range=,
    )
    if xlim:
        xaxis['range'] = xlim

    file_list = glob.glob(
        os.path.join(
            raw_simulator.get_raw_settings_value('SubtractedFilePath'),
            '*.dat'))
    sasm_list = raw_simulator.loadSASMs(file_list)

    data = [{
        'x': each_sasm.q,
        'y': each_sasm.i,
        'error_y': {
            'type': 'data',
            'array': each_sasm.err,
            'visible': errorbar_visible,
        },
        'type': 'line',
        'name': each_sasm.getParameter('filename'),
    } for each_sasm in sasm_list]

    figure = {
        'data': data,
        'layout': {
            'height': 500,
            'hovermode': 'closest',
            'title': TITLE[profile_name],
            'xaxis': xaxis,
            'yaxis': yaxis,
            # 'showlegend': True,
            # 'legend': {
            #     'x': 0,
            #     'y': -2,
            # },
        }
    }
    return figure


@dash_app.callback(
    Output('sasprofile-graph', 'figure'), [
        Input('sasprofile-plot-type', 'value'),
        Input('sasprofile-errorbar', 'value'),
        Input('sasprofile-xlim', 'value'),
    ])
def _update_graph(plot_type, errorbar_visible, xlim):
    return _get_figure(plot_type, errorbar_visible, xlim)
