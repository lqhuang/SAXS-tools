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

_CIRCLE_OPTIONS = [{
    'label': 'True',
    'value': True
}, {
    'label': 'False',
    'value': False
}]

_DEFAULT_FIGURE_LAYOUT = {
    'xaxis': dict(title='pixel', scaleanchor='y', constrain='domain'),
    'yaxis': dict(title='pixel', autorange='reversed'),
}


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
    html.Label('Show extra circle'),
    dcc.RadioItems(
        id='sasimage-circle-visible',
        options=_CIRCLE_OPTIONS,
        value=False,
        labelStyle=INLINE_LABEL_STYLE,
    ),
    html.Label('Radius of circle'),
    dcc.Slider(
        id='sasimage-circle-radius-slider',
        min=0,
        max=150,
        step=1,
        value=30,
    ),
])


def get_sasimage(exp):
    return _DEFAULT_LAYOUT


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
    return None


@dash_app.callback(
    Output('sasimage-file-selection-2', 'value'),
    [Input('sasimage-file-selection-2', 'options')])
def _update_selction_value_2(file_options):
    if isinstance(file_options, list) and file_options:
        return file_options[-1]['value']
    return None


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


def _update_image(
        plot_type,
        image_fname,
        colorbar_range,
        show_circle,
        circle_radius,
        info_json,
):
    exp = json.loads(info_json)['exp']
    image = raw_simulator.get_sasimage(exp, image_fname)

    if show_circle:
        circle_layout = {
            'shapes': [{  # unfilled circle
                'type': 'circle',
                'xref': 'x',
                'yref': 'y',
                'x0': center[0] - circle_radius,
                'y0': center[1] - circle_radius,
                'x1': center[0] + circle_radius,
                'y1': center[1] + circle_radius,
                'line': {
                    'color': 'rgba(225, 225, 225, 1)',
                },
            }],
        }
        circle_layout.update(_DEFAULT_FIGURE_LAYOUT)
        figure_layout = circle_layout
    else:
        figure_layout = _DEFAULT_FIGURE_LAYOUT

    return {
        'data': [{
            'type': plot_type,
            'z': image,
            'zmin': colorbar_range[0],
            'zmax': colorbar_range[1],
            'colorscale': 'Jet',
            'ncontours': 5,
        }],
        'layout': figure_layout,
    }  # yapf: disable


@dash_app.callback(
    Output('sasimage-graph-1', 'figure'),
    [
        Input('sasimage-plot-type-1', 'value'),
        Input('sasimage-file-selection-1', 'value'),
        Input('sasimage-colorbar-slider', 'value'),
        Input('sasimage-circle-visible', 'value'),
        Input('sasimage-circle-radius-slider', 'value'),
    ],
    [State('page-info', 'children')],
)
def _update_image_1(
        plot_type,
        image_fname,
        colorbar_range,
        show_circle,
        circle_radius,
        info_json,
):
    return _update_image(
        plot_type,
        image_fname,
        colorbar_range,
        show_circle,
        circle_radius,
        info_json,
    )


@dash_app.callback(
    Output('sasimage-graph-2', 'figure'),
    [
        Input('sasimage-plot-type-2', 'value'),
        Input('sasimage-file-selection-2', 'value'),
        Input('sasimage-colorbar-slider', 'value'),
        Input('sasimage-circle-visible', 'value'),
        Input('sasimage-circle-radius-slider', 'value'),
    ],
    [State('page-info', 'children')],
)
def _update_image_2(
        plot_type,
        image_fname,
        colorbar_range,
        show_circle,
        circle_radius,
        info_json,
):
    return _update_image(
        plot_type,
        image_fname,
        colorbar_range,
        show_circle,
        circle_radius,
        info_json,
    )
