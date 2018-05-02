from __future__ import print_function, division

from urllib import parse
import json

from dash.dependencies import Input, Output

from .base import dash_app
from .layouts import (get_sasimage, get_sasprofile, get_series_analysis,
                      get_cormap, get_gnom)


def get_graph_layout(exp, layout_type):
    if layout_type == 'sasimage':
        return get_sasimage(exp)
    elif layout_type == 'sasprofile':
        return get_sasprofile(exp)
    elif layout_type == 'cormap':
        return get_cormap(exp)
    elif layout_type == 'series_analysis':
        return get_series_analysis(exp)
    elif layout_type == 'guinier':
        return 'Not Implemented'
    elif layout_type == 'gnom':
        return get_gnom(exp)
    else:
        return '404'


@dash_app.callback(Output('page-content', 'children'), [Input('url', 'href')])
def display_page(href):
    if href is not None:
        query_result = parse.parse_qs(parse.urlparse(href).query)
        exp = query_result['exp'][0]
        layout_type = query_result['graph_type'][0]
        return get_graph_layout(exp, layout_type)
    else:
        return '404'


@dash_app.callback(Output('page-info', 'children'), [Input('url', 'href')])
def set_page_info(href):
    if href is not None:
        query_result = parse.parse_qs(parse.urlparse(href).query)
        exp = query_result['exp'][0]
        layout_type = query_result['graph_type'][0]
        return json.dumps({'exp': int(exp), 'layout_type': layout_type})
    else:
        return '404'


if __name__ == '__main__':
    dash_app.run_server(debug=False)
