from gevent import monkey
monkey.patch_all()

import os
import logging
import logging.config

from flask import Flask
from flask import Blueprint
from flask_restplus import Api
from dynaconf import FlaskDynaconf

from automoticz.extensions import *
from automoticz.cli import reset_migrations
from automoticz.utils.constants import ENV, CACHE_PIN_KEY, CACHE_SET_PIN_KEY, CACHE_GET_INFO_KEY
from automoticz.utils.oauth2 import get_default_credentials
from automoticz.tasks import get_beacon_pin, set_beacon_pin
from automoticz.settings_loader import load_celery_imports, load_api_endpoints

from automoticz.api.ws import *


def configure_app(app):
    '''
    Configure app settings.
    '''
    FlaskDynaconf(app)
    logging.config.fileConfig(app.config.LOGGING_SETTINGS)
    


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
    proximity.init_app(app)
    domoticz.init_app(app)
    cache.init_app(app)
    


def init_cli(app):
    '''
    Initialize cli commands.
    '''
    app.cli.add_command(reset_migrations)


def register_blueprints(app):
    '''
    Register blueprints for app.
    '''
    api_blueprint = Blueprint('api', __name__, url_prefix='/api')

    api = Api(api_blueprint,
              title='Automoticz API',
              version='1.0-dev',
              description='REST API for Automoticz system.')

    load_api_endpoints(app, api)
    app.register_blueprint(api_blueprint)


def init_celery(app=None, celery_context=False):
    '''
    Initialize Celery instance
    '''
    app = app or create_app(run_from_celery=celery_context)
    celery_app.conf.broker_url = app.config.CELERY_BROKER_URL
    celery_app.conf.result_backend = app.config.CELERY_RESULT_BACKEND
    celery_app.conf.task_default_queue = app.config.CELERY_TASK_DEFAULT_QUEUE
    celery_app.conf.update(app.config)

    class ContextTask(celery_app.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    celery_app.conf.imports = load_celery_imports(app, celery_app.conf.imports)
    celery_app.conf.task_serializer = 'json'
    celery_app.conf.result_serializer = 'pickle'
    celery_app.conf.accept_content = ['json', 'pickle']
    celery_app.finalize()
    return celery_app


def post_init(app):
    '''
    Post initialization.

    Ex. for disabling warnings.
    '''
    if app.config.ENV != ENV.PRODUCTION:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Surpassing warning when calling Domoticz API
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    with app.app_context():
        # Initializing Proximity Beacon API
        creds = get_default_credentials()
        proximity.init_api(creds)
        # Getting PIN and saving to cache if not present
        if not cache.get(CACHE_PIN_KEY):
            get_beacon_pin.delay()
        # If configuration requires reload pin attachment on
        # authentication beacon
        if app.config.RELOAD_PIN_ON_START:
            if not cache.get(CACHE_SET_PIN_KEY):
                set_beacon_pin.delay()


def init_socketio(app):
    socketio.init_app(
        app,
        message_queue=app.config.CELERY_BROKER_URL,
        async_mode="gevent_uwsgi",
        engineio_logger=True,
    )



def create_app(run_from_celery=False):
    ''' 
    Create new Flask app instance.
    '''
    app = Flask('automoticz')
    configure_app(app)
    init_extensions(app)
    register_blueprints(app)
    if not run_from_celery:
        init_socketio(app)
    init_celery(app)
    init_cli(app)
    post_init(app)
    return app
