from __future__ import print_function, division

import numpy as np
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import numpy as np
from .style import GRAPH_GLOBAL_CONFIG, INLINE_LABEL_STYLE
from ..base import dash_app

_PLOT_OPTIONS = [{
    'label': 'Heatmap',
    'value': 'heatmap'
}, {
    'label': 'Contour',
    'value': 'contour'
}]


def _six_columns(suffix, data, selection):
    """return html.Div content with six columns class.

    Parameters
    ---------
    selection: tuple, (options, value)

    Returns
    -------
    content: html.Div
    """
    return html.Div(
        children=[
            dcc.Graph(
                id='sasimage-graph-%s' % suffix,
                figure={
                    'data': data,
                    'layout': {},
                },
                config=GRAPH_GLOBAL_CONFIG,
            ),
            html.Label('Plot type'),
            dcc.RadioItems(
                id='sasimage-plot-type-%s' % suffix,
                options=_PLOT_OPTIONS,
                value='heatmap',
                labelStyle=INLINE_LABEL_STYLE,
            ),
            html.Label('Select image file to plot'),
            dcc.Dropdown(
                id='sasimage-file-selection-%s' % suffix,
                options=selection[0],
                value=selection[1],
            ),
        ],
        className="six columns",
    )


def _get_default_layout(exp):

    select_options = [{
        'label': 'First file',
        'value': '1'
    }, {
        'label': 'Second file',
        'value': '2'
    }, {
        'label': 'Third file',
        'value': '3'
    }]

    data1 = [{
        'id': 'sasimage-heatmap-1',
        'type': 'heatmap',
        'z': np.arange(0, 100, 0.01).reshape(100, 100),
        'zmin': 0,
        'zmax': 100,
    }]
    data2 = [{
        'id': 'sasimage-heatmap-2',
        'type': 'heatmap',
        'z': np.random.randint(0, 100, (100, 100)),
        'zmin': 0,
        'zmax': 100,
    }]

    layout = html.Div(children=[
        html.Div(
            children=[
                _six_columns('1', data1, (select_options, 1)),
                _six_columns('2', data2, (select_options, 3)),
            ],
            className="row",
        ),
        html.Label('Color bar range slider'),
        dcc.RangeSlider(
            id='sasimage-colorbar-slider',
            # count=1,
            # disabled=True,
            min=0,
            max=100,
            step=1,
            value=[10, 80],
        ),
    ])
    return layout


def get_sasimage(exp):
    return _get_default_layout(exp)


# Update whole figure
# https://community.plot.ly/t/is-it-possible-to-update-just-layout-not-whole-figure-of-graph-in-callback/8300/4
# Using state to input source data
# https://community.plot.ly/t/callback-with-one-of-the-input-matching-the-output-automatic-graph-height/5327/3


@dash_app.callback(
    Output('sasimage-graph-1', 'figure'),
    [
        Input('sasimage-plot-type-1', 'value'),
        Input('sasimage-colorbar-slider', 'value')
    ],
    [State('sasimage-graph-1', 'figure')],
)
def update_image_1(plot_type, colorbar_range, curr_figure):
    curr_figure['data'][0]['type'] = plot_type
    curr_figure['data'][0]['zmin'] = colorbar_range[0]
    curr_figure['data'][0]['zmax'] = colorbar_range[1]
    return curr_figure


@dash_app.callback(
    Output('sasimage-graph-2', 'figure'),
    [
        Input('sasimage-plot-type-2', 'value'),
        Input('sasimage-colorbar-slider', 'value')
    ],
    [State('sasimage-graph-2', 'figure')],
)
def update_image_2(plot_type, colorbar_range, curr_figure):
    curr_figure['data'][0]['type'] = plot_type
    curr_figure['data'][0]['zmin'] = colorbar_range[0]
    curr_figure['data'][0]['zmax'] = colorbar_range[1]
    return curr_figure
