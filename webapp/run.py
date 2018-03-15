from flask import Flask
from flask_bootstrap import Bootstrap
# from flask_script import Manager, Server
from views import index
import config


def init_blueprint(app):
    app.register_blueprint(index)


def create_app(app_config):
    app = Flask(
        __name__,
        # template_folder=None,
        # static_folder=None,
    )
    app.config.from_object(app_config)

    init_blueprint(app)

    Bootstrap(app)

    if app.debug:
        print(app.url_map)

    return app


if __name__ == '__main__':
    app = create_app(config)
    # manager = Manager(app)
    # manager.run()
    app.run(host='0.0.0.0')
