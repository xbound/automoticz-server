from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from automoticz.domoticz import DomoticzAPI

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
ma = Marshmallow()
domoticz = DomoticzAPI()

from automoticz.utils.beacons import ProximityBeaconAPI
beaconapi = ProximityBeaconAPI()