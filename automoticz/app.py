import os

from flask import Flask
from dynaconf import FlaskDynaconf

from automoticz.extensions import db
from automoticz.extensions import jwt
from automoticz.extensions import ma
from automoticz.extensions import migrate
from automoticz.cli import test
from automoticz.api.views import blueprint
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


def init_cli(app):
    '''
    Initialize cli commands.
    '''
    app.cli.add_command(test)


def register_blueprints(app):
    '''
    Register blueprints for app.
    '''
    app.register_blueprint(blueprint)


def create_app():
    ''' 
    Create new Flask app instance.
    '''
    app = Flask('automoticz')
    configure_app(app)
    init_extensions(app)
    register_blueprints(app)
    init_cli(app)
    return app
