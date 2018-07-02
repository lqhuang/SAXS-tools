from __future__ import print_function, division

import json

from numpy import log10, asarray
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from ..base import dash_app
from .style import GRAPH_GLOBAL_CONFIG, INLINE_LABEL_STYLE
from .style import YLABEL, LINE_STYLE

from ..datamodel import raw_simulator

_PLOT_OPTIONS = [{
    'label': 'Profile colormap',
    'value': 'colormap',
}, {
    'label': 'Cross slice',
    'value': 'crossline',
}]

_PROFILE_OPTIONS = [
    {
        'label': 'Intensity',
        'value': 'intensity'
    },
    {
        'label': 'Error',
        'value': 'error'
    },
]

_XLIM_MAX = 200

_DEFAULT_LAYOUT = html.Div(children=[
    dcc.Graph(
        id='colormap-graph',
        figure={},
        config=GRAPH_GLOBAL_CONFIG,
    ),
    html.Label('Plot type'),
    dcc.RadioItems(
        id='colormap-plot-type',
        options=_PLOT_OPTIONS,
        value='colormap',
        labelStyle=INLINE_LABEL_STYLE,
    ),
    html.Label('Profile type'),
    dcc.RadioItems(
        id='colormap-profile-type',
        options=_PROFILE_OPTIONS,
        value='intensity',
        labelStyle=INLINE_LABEL_STYLE,
    ),
    html.Label('Slider for q slice'),
    dcc.Slider(
        id='colormap-q-slice',
        # count=1,
        # disabled=True,
        min=0,
        max=_XLIM_MAX,
        step=1,
        value=0,
    ),
])


def get_colormap(exp):
    return _DEFAULT_LAYOUT


def _get_figure(exp, plot_type, profile_type, q_idx):
    sasm_list = raw_simulator.get_sasprofile(exp)

    # TODO: Fix length of q vector. Use new SASM method.

    if plot_type == 'colormap':
        if profile_type == 'intensity':
            image = [each.i[0:100] for each in sasm_list]
        elif profile_type == 'error':
            image = [each.err[0:100] for each in sasm_list]
        curr_q = sasm_list[0].q[100]
        return {
            'data': [{
                'type': 'heatmap',
                'z': log10(asarray(image)),
                # 'zmin': colorbar_range[0],
                # 'zmax': colorbar_range[1],
                'colorscale': 'Jet',
                'ncontours': 5,
            }],
            'layout':  {
                'title': dict(title='Colormap (log scale) (max q={:.4} 1/angstrom)'.format(curr_q)),
                'xaxis': dict(title='sequence', scaleanchor='y', constrain='domain'),
                'yaxis': dict(title='q index', autorange='reversed'),
            },
        }  # yapf: disable

    elif plot_type == 'crossline':
        if profile_type == 'intensity':
            profile = [sasm.i[q_idx] for sasm in sasm_list]
        elif profile_type == 'error':
            profile = [sasm.err[q_idx] for sasm in sasm_list]
        curr_q = sasm_list[0].q[q_idx]

        xaxis = dict(title='Index for sas profile')
        if profile_type == 'intensity':
            yaxis = dict(title=YLABEL['linear'])
        elif profile_type == 'error':
            yaxis = dict(title=YLABEL['error'])

        return {
            'data': [{
                'x': list(range(len(profile))),
                'y': profile,
                'type': 'line',
                'line': LINE_STYLE,
                'name': 'q={:.3f}'.format(curr_q),
            }],
            'layout': {
                'height': 500,
                'hovermode': 'closest',
                'xaxis': xaxis,
                'yaxis': yaxis,
                'title': 'Cross slice for the same q idx (q={:.4f} 1/angstrom)'.format(curr_q),
            }
        }  # yapf: disable


@dash_app.callback(
    Output('colormap-graph', 'figure'),
    [
        Input('colormap-plot-type', 'value'),
        Input('colormap-profile-type', 'value'),
        Input('colormap-q-slice', 'value'),
    ],
    [State('page-info', 'children')],
)
def _update_graph(plot_type, profile_type, q_idx, info_json):
    exp = json.loads(info_json)['exp']
    return _get_figure(exp, plot_type, profile_type, q_idx)


@dash_app.callback(
    Output('colormap-q-slice', 'disabled'),
    [Input('colormap-plot-type', 'value')])
def _update_slider(plot_type):
    if plot_type == 'colormap':
        return True
    else:
        return False
