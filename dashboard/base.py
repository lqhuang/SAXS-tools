from __future__ import print_function, division

import dash
import dash_core_components as dcc
import dash_html_components as html

from webapp.app import flask_app, DASH_URL_BASE

dash_app = dash.Dash(
    __name__, server=flask_app, url_base_pathname=DASH_URL_BASE)
# flask_app = dash_app.server
dash_app.config.update({
    'suppress_callback_exceptions': True,
})
# dash_app.css.config.serve_locally = True
# dash_app.scripts.config.serve_locally = True

default_styles = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
dash_app.css.append_css({
    'external_url': default_styles,
})

extra_css = '/static/css/dash.css'
dash_app.css.append_css({
    'external_url': extra_css,
})

dash_app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
