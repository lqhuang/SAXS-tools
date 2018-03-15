from __future__ import print_function, division

import os
import sys
import glob

import numpy as np
import dash_core_components as dcc
import dash_html_components as html

from .style import GRAPH_GLOBAL_CONFIG

z = np.eye(10)
layout = html.Div(children=[
    dcc.Graph(
        id='profiles',
        figure={
            'type': 'heatmap',
            'data': {
                'z': z,
            },
            'layout': {
                'height': 800,
                'hovermode': 'closest',
                'title': 'Subtracted profiles',
                'xaxis': dict(title='frames'),
                'yaxis': dict(title='frames'),
            }
        },
        config=GRAPH_GLOBAL_CONFIG,
    ),
])


def get_cormap(exp):
    return layout
