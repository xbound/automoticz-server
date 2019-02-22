from flask import Blueprint
from flask_restplus import Api

from automoticz.api.endpoints import *

oauth2_blueprint = Blueprint('oauth2', __name__, url_prefix='/oauth2')

from automoticz.api.oauth2 import *

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    api_blueprint,
    title='Automoticz API',
    version='1.0-dev',
    description='REST API for automoticz.')

api.add_namespace(ping_namespace, path='/ping')
api.add_namespace(auth_namespace, path='/auth')