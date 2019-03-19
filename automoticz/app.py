import os

from flask import Flask
from dynaconf import FlaskDynaconf

from automoticz.extensions import *
from automoticz.cli import test
from automoticz.cli import reset_migrations
from automoticz.api.views import api_blueprint
from automoticz.api.views import oauth2_blueprint
from automoticz.utils.constants import ENV


def configure_app(app):
    '''
    Configure app settings.
    '''
    FlaskDynaconf(app)


def init_extensions(app):
    '''
    Initialize Flask extensions.
    '''
    db.init_app(app)
    if app.config.ENV != ENV.TESTING:
        migrate.init_app(app, db)
    else:
        with app.app_context():
            db.create_all()
    jwt.init_app(app)
    ma.init_app(app)
    beaconapi.init_app(app)
    domoticz.init_app(app)


def init_cli(app):
    '''
    Initialize cli commands.
    '''
    app.cli.add_command(test)
    app.cli.add_command(reset_migrations)


def register_blueprints(app):
    '''
    Register blueprints for app.
    '''
    app.register_blueprint(api_blueprint)
    app.register_blueprint(oauth2_blueprint)


def post_init(app):
    '''
    Set environmental variables for Google OAuth2
    '''
    if app.config.ENV != ENV.PRODUCTION:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Surpassing warning when calling Domoticz API
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def create_app():
    ''' 
    Create new Flask app instance.
    '''
    app = Flask('automoticz')
    configure_app(app)
    init_extensions(app)
    register_blueprints(app)
    init_cli(app)
    post_init(app)
    return app
