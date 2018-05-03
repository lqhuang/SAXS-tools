from __future__ import print_function, division

import json

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from .style import GRAPH_GLOBAL_CONFIG, INLINE_LABEL_STYLE
from ..base import dash_app
from ..datamodel import raw_simulator

_PLOT_OPTIONS = [{
    'label': 'Adj Pr(>C) value',
    'value': 'adj Pr(>C)',
}, {
    'label': 'C value',
    'value': 'C',
}]

_DEFAULT_LAYOUT = html.Div(children=[
    dcc.Graph(
        id='cormap-graph',
        figure={},
        config=GRAPH_GLOBAL_CONFIG,
    ),
    html.Label('Plot type'),
    dcc.RadioItems(
        id='cormap-plot-type',
        options=_PLOT_OPTIONS,
        value='adj Pr(>C)',
        labelStyle=INLINE_LABEL_STYLE,
    ),
])


def get_cormap(exp):
    return _DEFAULT_LAYOUT


_DEFAULT_FIGURE_LAYOUT = {
    'height': 550,
    'hovermode': 'closest',
    'title': 'CorMap Heatmap',
    'xaxis': dict(title='Frames', scaleanchor='y', constrain='domain'),
    'yaxis': dict(title='Frames', autorange='reversed'),
}


@dash_app.callback(
    Output('cormap-graph', 'figure'),
    [
        Input('cormap-plot-type', 'value'),
        Input('page-info', 'children'),
    ],
)
def _update_figure(plot_type, info_json):
    exp = json.loads(info_json)['exp']
    cormap_heatmap = raw_simulator.get_cormap_heatmap(exp, plot_type)

    if plot_type == 'C':
        colorscale = 'Jet'
        colorbar = dict()
    else:
        p_threshold = 0.01  # default
        colorscale = (
            (0.0, "#D55E00"),  # orange
            (p_threshold, "#D55E00"),
            (p_threshold, "#009E73"),  # green
            (0.99999999, "#009E73"),
            (1, "#0072B2"),  # blue
        )
        colorbar = dict(
            tickmode='array',
            tickvals=(0, (p_threshold + 1.0) / 2.0, 1.0),
            ticktext=(
                'adj Pr(>C) < 0.01',
                '0.01 <= adj Pr(>C) < 1',
                'adj Pr(>C) == 1',
            ),
        )
    return {
        'data': [{
            'type': 'heatmap',
            'z': cormap_heatmap,
            'colorscale': colorscale,
            'colorbar': colorbar,
        }],
        'layout': _DEFAULT_FIGURE_LAYOUT,
    } # yapf: disable
