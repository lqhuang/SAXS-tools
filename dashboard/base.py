from __future__ import print_function, division

import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import url_for

from webapp.app import flask_app, DASH_URL_BASE

dash_app = dash.Dash(
    __name__, server=flask_app, url_base_pathname=DASH_URL_BASE)
# flask_app = dash_app.server

dash_app.config.update({
    # Since we're adding callbacks to elements that don't exist in the
    # app.layout, Dash will raise an exception to warn us that we might
    # be doing something wrong. In this case, we're adding the elements
    # through a callback, so we can ignore the exception.
    'suppress_callback_exceptions': True,
})
dash_app.css.config.serve_locally = True
dash_app.scripts.config.serve_locally = True

dash_app.layout = html.Div(children=[
    # fix this hard coding path (/static)
    html.Link(rel='stylesheet', href='/static/css/bWLwgP.css'),
    html.Link(rel='stylesheet', href='/static/css/dash.css'),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
