from __future__ import print_function, division

from flask import Flask
from flask_bootstrap import Bootstrap
# from flask_script import Manager, Server

from .views import index, exp_pages
from . import config


def init_blueprint(app):
    app.register_blueprint(index)
    app.register_blueprint(exp_pages)


def create_app(flask_config):
    app = Flask(__name__)
    app.config.from_object(flask_config)

    init_blueprint(app)

    Bootstrap(app)

    if app.debug:
        print(app.url_map)

    return app


DASH_URL_BASE = '/dashboard'
flask_app = create_app(config)

if __name__ == '__main__':
    flask_app = create_app(config)
    # manager = Manager(app)
    # manager.run()
    flask_app.run(host='0.0.0.0')
