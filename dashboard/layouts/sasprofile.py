from __future__ import print_function, division

import json

from numpy import log2, log10
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Th, Tr, Td
from dash.dependencies import Input, Output, State

from .style import XLABEL, YLABEL, TITLE, LINE_STYLE
from .style import ERRORBAR_OPTIONS
from .style import INLINE_LABEL_STYLE, GRAPH_GLOBAL_CONFIG
from ..base import dash_app
from ..datamodel import raw_simulator

# axis scale for (yaxis, xaxis)
# _LIN_LIN = ['linear', 'linear']
# _LOG_LIN = ['log', 'linear']
# _LOG_LOG = ['log', 'log']
# _LIN_LOG = ['linear', 'log']

# axis scale for (yaxis, xaxis)
_LIN_LIN = 'linear-linear'
_LOG_LIN = 'log-linear'
_LOG_LOG = 'log-log'
_LIN_LOG = 'linear-log'

_XLIM_MAX = 0.20
_SLIDER_POINTS = 200

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

_CALC_FUNCTION = {
    'sasprofile': {
        'q': lambda q: q,
        'i': lambda q, i: i,
    },
    'guinier': {
        'q': lambda q: q**2.0,
        'i': lambda q, i: log2(i),  # in ln scale
    },
    'kratky': {
        'q': lambda q: q,
        'i': lambda q, i: i * q**2.0,
    },
    'porod': {
        'q': lambda q: q**4.0,
        'i': lambda q, i: i * q**4.0,
    },
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
    html.Label(
        "Show error bar (Always be false with Guinier, Kratky and Porod plot.)"),
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
        max=_XLIM_MAX,
        step=0.01,
        value=[0.0, 0.20],
    ),
])


def get_sasprofile(exp):
    return _DEFAULT_LAYOUT


def _get_figure(exp, plot_type, errorbar_visible, xlim=None):
    profile_name = plot_type if '-' not in plot_type else 'sasprofile'

    if profile_name == 'sasprofile':
        ylabel, xlabel = plot_type.split('-')  # eg: 'log-log'
        xaxis = dict(
            title=XLABEL[xlabel],
            type=xlabel,
        )
        yaxis = dict(
            title=YLABEL[ylabel],
            type=ylabel,
        )
    else:
        errorbar_visible = False
        ylabel, xlabel = 'linear', 'linear'
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

    data = [{
        'x': _CALC_FUNCTION[profile_name]['q'](each_sasm.q),
        'y': _CALC_FUNCTION[profile_name]['i'](each_sasm.q, each_sasm.i),
        'error_y': {
            'type': 'data',
            'array': each_sasm.err,
            'visible': errorbar_visible,
        },
        'type': 'line',
        'line': LINE_STYLE,
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


# @dash_app.callback(
#     Output('sasprofile-xlim', 'max'), [
#         Input('sasprofile-plot-type', 'value'),
#     ])
# def _update_xlim_slider_max(plot_type):
#     if '-' not in plot_type:
#         return _CALC_FUNCTION[plot_type]['q'](_XLIM_MAX)
#     else:
#         _, xaxis = plot_type.split('-')
#         if xaxis == 'log':
#             return log10(_XLIM_MAX)


# @dash_app.callback(
#     Output('sasprofile-xlim', 'min'), [
#         Input('sasprofile-plot-type', 'value'),
#     ])
# def _update_xlim_slider_min(plot_type):
#     if '-' not in plot_type:
#         return 0.0
#     else:
#         _, xaxis = plot_type.split('-')
#         if xaxis == 'log':
#             return log10(1e-3)


# @dash_app.callback(
#     Output('sasprofile-xlim', 'step'), [
#         Input('sasprofile-xlim', 'min'),
#         Input('sasprofile-xlim', 'max'),
#     ])
# def _update_xlim_slider_step(curr_min, curr_max):
#     print('curr_min', curr_min)
#     print('curr_max', curr_max)
#     print('step:', (curr_max - curr_min) / 200.0)
#     print('step:', (curr_max - curr_min) / 200.0)
#     print('step:', (curr_max - curr_min) / 200.0)
#     print('step:', (curr_max - curr_min) / 200.0)
#     return (curr_max - curr_min) / _SLIDER_POINTS


# @dash_app.callback(
#     Output('sasprofile-xlim', 'value'), [
#         Input('sasprofile-plot-type', 'value'),
#     ])
# def _update_xlim_slider_value(plot_type):
#     if '-' not in plot_type:
#         new_value = (0.0, _CALC_FUNCTION[plot_type]['q'](_XLIM_MAX))
#     else:
#         _, xaxis = plot_type.split('-')
#         if xaxis == 'log':
#             new_value = (log10(1e-3), log10(_XLIM_MAX))
#         else:
#             new_value = (0.0, _XLIM_MAX)
#     print('new_range:', new_value)
#     print('new_range:', new_value)
#     print('new_range:', new_value)
#     print('new_range:', new_value)
#     print('new_range:', new_value)
#     return new_value


@dash_app.callback(
    Output('sasprofile-graph', 'figure'),
    [
        Input('sasprofile-plot-type', 'value'),
        Input('sasprofile-errorbar', 'value'),
        Input('sasprofile-xlim', 'value'),
    ],
    [State('page-info', 'children')],
)
def _update_graph(plot_type, errorbar_visible, curr_xlim, info_json):
    info_dict = json.loads(info_json)
    exp = info_dict['exp']
    return _get_figure(exp, plot_type, errorbar_visible, curr_xlim)
