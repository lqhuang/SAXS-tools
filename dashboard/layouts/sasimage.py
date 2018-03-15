from __future__ import print_function, division

import numpy as np
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import numpy as np
from .style import GRAPH_GLOBAL_CONFIG
from ..base import dash_app

SELECT_OPTIONS = [{
    'label': 'First file',
    'value': '1'
}, {
    'label': 'Second file',
    'value': '2'
}, {
    'label': 'Third file',
    'value': '3'
}]

data = [{'z': np.eye(100), 'type': 'heatmap'}]

layout = html.Div(children=[
    html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Graph(
                        id='sasimage-graph-1',
                        figure={
                            'data': data,
                            'layout': {},
                        },
                        config=GRAPH_GLOBAL_CONFIG,
                    ),
                    html.Label('Plot type'),
                    dcc.Dropdown(
                        id='sasimage-file-selection-1',
                        options=SELECT_OPTIONS,
                        value=SELECT_OPTIONS[0]['value'],
                    ),
                ],
                className="six columns",
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id='sasimage-graph-2',
                        figure={
                            'data': data,
                            'layout': {},
                        },
                        config=GRAPH_GLOBAL_CONFIG,
                    ),
                    html.Label('Plot type'),
                    dcc.Dropdown(
                        id='sasimage-file-selection-2',
                        options=SELECT_OPTIONS,
                        value=SELECT_OPTIONS[0]['value'],
                    ),
                ],
                className="six columns",
            ),
        ],
        className="row",
    ),
    html.Label('Color bar range slider'),
    dcc.RangeSlider(
        id='sasimage-colorbar-slider',
        count=1,
        min=-5,
        max=10,
        step=0.5,
        value=[-3, 7],
    ),
])


def get_sasimage(exp):
    return layout


@dash_app.callback(
    Output('sasimage-graph-1', 'figure'), [
        Input('sasimage-file-selection-1', 'value'),
        Input('sasimage-colorbar-slider', 'value'),
    ])
def update_image_1(filename, colorbar_range):
    return np.eye(10)


@dash_app.callback(
    Output('sasimage-graph-2', 'figure'), [
        Input('sasimage-file-selection-2', 'value'),
        Input('sasimage-colorbar-slider', 'value'),
    ])
def update_image_2(filename, colorbar_range):
    return np.eye(10)
