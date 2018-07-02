from __future__ import print_function, division

from flask import Flask
from flask_bootstrap import Bootstrap

from .views import index, exp_pages, playground, features
from . import config


def init_blueprint(app):
    app.register_blueprint(index)
    app.register_blueprint(exp_pages)
    app.register_blueprint(playground)
    app.register_blueprint(features)


def create_app(flask_config):
    app = Flask(__name__)
    app.config.from_object(flask_config)
    app.url_map.strict_slashes = False

    init_blueprint(app)

    Bootstrap(app)

    if app.debug:
        print(app.url_map)

    return app


DASH_URL_BASE = '/dashboard'
flask_app = create_app(config)

if __name__ == '__main__':
    flask_app = create_app(config)
    flask_app.run(host='0.0.0.0')
