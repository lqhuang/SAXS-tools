from __future__ import print_function, division

from urllib import parse

from dash.dependencies import Input, Output

from .base import dash_app
from .layouts import get_sasimage, get_sasprofile, get_cormap, get_gnom


def get_layout(exp, layout_type):
    if layout_type == 'sasimage':
        return get_sasimage(exp)
    elif layout_type == 'sasprofile':
        return get_sasprofile(exp)
    elif layout_type == 'cormap':
        return get_cormap(exp)
    elif layout_type == 'guinier':
        return '404'
    elif layout_type == 'gnom':
        return get_gnom(exp)
    else:
        return '404'


@dash_app.callback(Output('page-content', 'children'), [Input('url', 'href')])
def display_page(href):
    if href is not None:
        query_result = parse.parse_qs(parse.urlparse(href).query)
        exp = query_result['exp']
        layout_type = query_result['graph_type'][0]
        return get_layout(exp, layout_type)
    else:
        return '404'


if __name__ == '__main__':
    dash_app.run_server(debug=False)
