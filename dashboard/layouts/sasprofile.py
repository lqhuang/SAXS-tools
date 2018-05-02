from __future__ import print_function, division

import json

from numpy import log2
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Th, Tr, Td
from dash.dependencies import Input, Output, State

from .style import XLABEL, YLABEL, TITLE
from .style import ERRORBAR_OPTIONS
from .style import INLINE_LABEL_STYLE, GRAPH_GLOBAL_CONFIG
from ..base import dash_app
from ..datamodel import raw_simulator

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

_CALC_FUNCTION = dict()
_CALC_FUNCTION['guinier'] = {
    'q': lambda q: q**2.0,
    'i': lambda q, i: log2(i),  # in ln scale
}
_CALC_FUNCTION['kratky'] = {
    'q': lambda q: q,
    'i': lambda q, i: i * q**2.0,
}
_CALC_FUNCTION['porod'] = {
    'q': lambda q: q**4.0,
    'i': lambda q, i: i * q**4.0,
}

_line_style_table = html.Table(children=[
    html.Thead([
        Th('Curves'),
        Th('Marker'),
        Th('Linestyle'),
        Th('Removed'),
    ]),
    Tr([
        Td('curve 1'),
        Td('2'),
        Td('3'),
        Td('4'),
    ]),
    Tr([
        Td('curve 2'),
        Td('6'),
        Td('7'),
        Td('8'),
    ]),
])

_DEFAULT_PLOT_TYPE = _LOG_LIN

_DEFAULT_LAYOUT = html.Div(children=[
    dcc.Graph(
        id='sasprofile-graph',
        figure={},
        config=GRAPH_GLOBAL_CONFIG,
    ),
    html.Details(children=[
        html.Summary('Label of the item'),
        html.Div(children=_line_style_table),
    ]),
    html.Label('Plot type'),
    dcc.RadioItems(
        id='sasprofile-plot-type',
        options=_PLOT_OPTIONS,
        value=_DEFAULT_PLOT_TYPE,
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


def get_sasprofile(exp):
    return _DEFAULT_LAYOUT


def _get_figure(exp, plot_type, errorbar_visible, xlim=None):
    profile_name = plot_type if isinstance(plot_type, str) else 'sasprofile'
    if profile_name == 'sasprofile':
        ylabel, xlabel = plot_type  # tuple
        xaxis = dict(
            title=XLABEL[xlabel],
            type=xlabel,
            # range=[0.0, xlim],
        )
        yaxis = dict(
            title=YLABEL[ylabel],
            type=ylabel,
            # range=,
        )
    else:
        ylabel, xlabel = 'linear', 'linear'
        errorbar_visible = False
        xaxis = dict(
            title=XLABEL[profile_name],
            type=xlabel,
        )
        yaxis = dict(
            title=YLABEL[profile_name],
            type=ylabel,
        )
    if xlim:
        xaxis['range'] = xlim

    sasm_list = raw_simulator.get_sasprofile(exp)

    if profile_name == 'sasprofile':
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
    else:
        data = [{
            'x': _CALC_FUNCTION[plot_type]['q'](each_sasm.q),
            'y': _CALC_FUNCTION[plot_type]['i'](each_sasm.q, each_sasm.i),
            'error_y': {
                'type': 'data',
                'array': each_sasm.err,
                'visible': errorbar_visible,
            },
            'type': 'line',
            'name': each_sasm.getParameter('filename'),
        } for each_sasm in sasm_list]

    return {
        'data': data,
        'layout': {
            'height': 500,
            'hovermode': 'closest',
            'title': TITLE[profile_name],
            'xaxis': xaxis,
            'yaxis': yaxis,
        }
    }


@dash_app.callback(
    Output('sasprofile-graph', 'figure'),
    [
        Input('sasprofile-plot-type', 'value'),
        Input('sasprofile-errorbar', 'value'),
        Input('sasprofile-xlim', 'value'),
    ],
    [State('page-info', 'children')],
)
def _update_graph(plot_type, errorbar_visible, xlim, info_json):
    info_dict = json.loads(info_json)
    exp = info_dict['exp']
    return _get_figure(exp, plot_type, errorbar_visible, xlim)
