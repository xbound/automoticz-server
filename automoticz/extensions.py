from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from celery import Celery

from automoticz.domoticz import DomoticzAPI

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
cache = Cache()
domoticz = DomoticzAPI()
celery_app = Celery()

from automoticz.utils.beacons import ProximityBeaconAPI
beaconapi = ProximityBeaconAPI()