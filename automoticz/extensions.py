import logging

from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from celery import Celery


db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
cache = Cache()
socketio = SocketIO()
celery_app = Celery()

from automoticz.plugins.domoticz import DomoticzAPI
domoticz = DomoticzAPI()

from automoticz.plugins.proximity import ProximityBeaconAPI
proximity = ProximityBeaconAPI()


def get_logger():
    return logging.getLogger()
