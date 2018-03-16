from __future__ import print_function, division

import os
import glob

import dash_core_components as dcc
import dash_html_components as html

from .datamodel import raw_simulator
from .style import XLABEL, YLABEL

layout = html.Div(children=[
    dcc.Graph(
        id='gnom-graph',
        figure={
            'data': [],
            'layout': {
                'height': 500,
                'hovermode': 'closest',
                'title': 'Subtracted profiles',
                'xaxis': dict(title=XLABEL['distance']),
                'yaxis': dict(title=YLABEL['pr']),
            }
        },
    ),
])


def get_gnom(exp):
    file_list = glob.glob(
        os.path.join(
            raw_simulator.get_raw_settings_value('GnomFilePath'), '*.out'))

    iftm_list = raw_simulator.loadIFTMs(file_list)

    # xlim = iftm.getQrange()

    data = [{
        'x': each_iftm.r,
        'y': each_iftm.p,
        'type': 'line',
        'name': each_iftm.getParameter('filename')
    } for each_iftm in iftm_list]

    layout.children[0].figure['data'] = data

    return layout