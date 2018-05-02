from __future__ import print_function, division

import os.path
import json

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from .style import GRAPH_GLOBAL_CONFIG, INLINE_LABEL_STYLE
from ..base import dash_app
from ..datamodel import raw_simulator

_PLOT_OPTIONS = [{
    'label': 'Heatmap',
    'value': 'heatmap'
}, {
    'label': 'Contour',
    'value': 'contour'
}]

_DEFAULT_FIGURE_LAYOUT = {'yaxis': dict(autorange='reversed')}


def _six_columns(suffix: str):
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
                id='sasimage-graph-%s' % str(suffix),
                figure={},
                config=GRAPH_GLOBAL_CONFIG,
            ),
            html.Label('Plot type'),
            dcc.RadioItems(
                id='sasimage-plot-type-%s' % str(suffix),
                options=_PLOT_OPTIONS,
                value='heatmap',
                labelStyle=INLINE_LABEL_STYLE,
            ),
            html.Label('Select image file to plot'),
            dcc.Dropdown(
                id='sasimage-file-selection-%s' % str(suffix),
                options=[],
                value=None,
            ),
        ],
        className="six columns",
    )


_DEFAULT_LAYOUT = html.Div(children=[
    html.Div(
        children=[
            _six_columns('1'),
            _six_columns('2'),
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


def get_sasimage(exp):
    return _DEFAULT_LAYOUT


# Update whole figure
# https://community.plot.ly/t/is-it-possible-to-update-just-layout-not-whole-figure-of-graph-in-callback/8300/4
# Using state to input source data
# https://community.plot.ly/t/callback-with-one-of-the-input-matching-the-output-automatic-graph-height/5327/3


@dash_app.callback(
    Output('sasimage-file-selection-1', 'options'),
    [
        Input('page-info', 'children'),
        Input('sasimage-colorbar-slider', 'step'),
    ],  # FIXME: bug????
)
def _update_file_selction_1(info_json, useless):
    exp = json.loads(info_json)['exp']
    file_list = raw_simulator.get_files(exp, 'image_files')
    file_basename = (os.path.basename(i) for i in file_list)
    file_options = [{'label': i, 'value': i} for i in file_basename]
    return file_options


@dash_app.callback(
    Output('sasimage-file-selection-2', 'options'),
    [Input('sasimage-file-selection-1', 'options')])
def _update_selction_options_2(file_options):
    return file_options


@dash_app.callback(
    Output('sasimage-file-selection-1', 'value'),
    [Input('sasimage-file-selection-1', 'options')])
def _update_selction_value_1(file_options):
    if isinstance(file_options, list) and file_options:
        return file_options[0]['value']


@dash_app.callback(
    Output('sasimage-file-selection-2', 'value'),
    [Input('sasimage-file-selection-2', 'options')])
def _update_selction_value_2(file_options):
    if isinstance(file_options, list) and file_options:
        return file_options[-1]['value']


@dash_app.callback(
    Output('sasimage-colorbar-slider', 'min'), [
        Input('sasimage-file-selection-1', 'value'),
        Input('sasimage-file-selection-2', 'value'),
    ], [State('page-info', 'children')])
def _set_colorbar_range(image_fname_1, image_fname_2, info_json):
    exp = json.loads(info_json)['exp']
    image_1 = raw_simulator.get_sasimage(exp, image_fname_1)
    image_2 = raw_simulator.get_sasimage(exp, image_fname_2)
    return min(image_1.min(), image_2.min())


@dash_app.callback(
    Output('sasimage-colorbar-slider', 'max'), [
        Input('sasimage-file-selection-1', 'value'),
        Input('sasimage-file-selection-2', 'value'),
    ], [State('page-info', 'children')])
def _set_colorbar_range(image_fname_1, image_fname_2, info_json):
    exp = json.loads(info_json)['exp']
    image_1 = raw_simulator.get_sasimage(exp, image_fname_1)
    image_2 = raw_simulator.get_sasimage(exp, image_fname_2)
    return max(image_1.max(), image_2.max())


# @dash_app.callback(
#     Output('sasimage-colorbar-slider', 'value'), [
#         Input('sasimage-file-selection-1', 'value'),
#         Input('sasimage-file-selection-2', 'value'),
#     ], [State('page-info', 'children')])
# def _set_colorbar_range(image_fname_1, image_fname_2, info_json):
#     exp = json.loads(info_json)['exp']
#     image_1 = raw_simulator.get_sasimage(exp, image_fname_1)
#     image_2 = raw_simulator.get_sasimage(exp, image_fname_2)
#     lower_bound = min(image_1.min(), image_2.min())
#     upper_bound = max(image_1.max(), image_2.max())
#     return [lower_bound, upper_bound]


@dash_app.callback(
    Output('sasimage-graph-1', 'figure'),
    [
        Input('sasimage-plot-type-1', 'value'),
        Input('sasimage-file-selection-1', 'value'),
        Input('sasimage-colorbar-slider', 'value')
    ],
    [State('page-info', 'children')],
)
def _update_image_1(plot_type, image_fname, colorbar_range, info_json):
    exp = json.loads(info_json)['exp']
    image = raw_simulator.get_sasimage(exp, image_fname)
    return {
        'data': [{
            'type': plot_type,
            'z': image,
            'zmin': colorbar_range[0],
            'zmax': colorbar_range[1],
            'colorscale': 'Jet',
        }],
        'layout': _DEFAULT_FIGURE_LAYOUT,
    }  # yapf: disable


@dash_app.callback(
    Output('sasimage-graph-2', 'figure'),
    [
        Input('sasimage-plot-type-2', 'value'),
        Input('sasimage-file-selection-2', 'value'),
        Input('sasimage-colorbar-slider', 'value')
    ],
    [State('page-info', 'children')],
)
def _update_image_2(plot_type, image_fname, colorbar_range, info_json):
    exp = json.loads(info_json)['exp']
    image = raw_simulator.get_sasimage(exp, image_fname)
    return {
        'data': [{
            'type': plot_type,
            'z': image,
            'zmin': colorbar_range[0],
            'zmax': colorbar_range[1],
            'colorscale': 'Jet',
        }],
        'layout': _DEFAULT_FIGURE_LAYOUT,
    }  # yapf: disable
