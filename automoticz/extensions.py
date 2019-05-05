from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from celery import Celery


db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
cache = Cache()
celery_app = Celery()

from automoticz.plugins.domoticz import DomoticzAPI
domoticz = DomoticzAPI()

from automoticz.plugins.proximity import ProximityBeaconAPI
proximity = ProximityBeaconAPI()