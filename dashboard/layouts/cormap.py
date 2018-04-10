from __future__ import print_function, division

import numpy as np
import dash_core_components as dcc
import dash_html_components as html

from .style import GRAPH_GLOBAL_CONFIG, INLINE_LABEL_STYLE

_PLOT_OPTIONS = [{
    'label': 'Adj P(>C) value',
    'value': 'p_value',
}, {
    'label': 'C value',
    'value': 'c_value',
}]


def _get_default_layout(exp):
    layout = html.Div(children=[
        dcc.Graph(
            id='cormap-graph',
            figure=_get_figure(),
            config=GRAPH_GLOBAL_CONFIG,
        ),
        html.Label('Plot type'),
        dcc.RadioItems(
            id='cormap-plot-type',
            options=_PLOT_OPTIONS,
            value='p_value',
            labelStyle=INLINE_LABEL_STYLE,
        ),
    ])
    return layout


def _get_figure():
    z = np.eye(100)

    graph_layout = {
        'height': 600,
        'hovermode': 'closest',
        'title': 'CorMap',
        'xaxis': dict(title='Frames', scaleanchor='y', constrain='domain'),
        'yaxis': dict(title='Frames', autorange='reversed')
    }

    data = [{
        'type': 'heatmap',
        'z': z,
    }]

    figure = {
        'data': data,
        'layout': graph_layout,
    }
    return figure


def get_cormap(exp):
    return _get_default_layout(exp)
