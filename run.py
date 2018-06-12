from __future__ import print_function, division

from webapp.app import flask_app
from dashboard.app import dash_app

# from werkzeug.wsgi import DispatcherMiddleware

# flask_app.wsgi_app = DispatcherMiddleware(flask_app, {'/dash_app': dash_app.server})

if __name__ == '__main__':
    # dash_app.run_server()
    flask_app.run(host='0.0.0.0')
