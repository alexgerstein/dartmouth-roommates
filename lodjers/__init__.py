import os
import redis
from flask import Flask


def create_app(env=None):
    app = Flask(__name__, instance_relative_config=True,
                template_folder='frontend/templates',
                static_folder='frontend/static')

    # Load the default configuration
    app.config.from_object('config.default')

    # Load the configuration from the instance folder
    app.config.from_pyfile('config.py', silent=True)

    # Load the file specified by the APP_CONFIG_FILE environment variable
    # Variables defined here will override those in the default configuration
    env_config_file = os.environ.get('APP_CONFIG_FILE') or env

    if env_config_file:
        app.config.from_object('config.%s' % env_config_file)

    from lodjers.database import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from lodjers.mail import mail
    mail.init_app(app)

    from lodjers.login import flask_cas, login_manager
    app.register_blueprint(flask_cas)
    login_manager.init_app(app)

    from lodjers.frontend import frontend, assets
    app.register_blueprint(frontend.bp)
    assets.init_app(app)

    from lodjers.api import bp as api_bp
    app.register_blueprint(api_bp)

    return app


def create_redis_connection(env=None):
    return redis.from_url(os.getenv('REDISTOGO_URL')) if env == "staging" \
           else redis.Redis()
