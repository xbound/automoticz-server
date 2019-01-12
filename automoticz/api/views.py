from flask import Blueprint
from flask_restplus import Api

from automoticz.api.endpoints import *

blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    blueprint,
    title='Automoticz API',
    version='1.0-dev',
    description='REST API for automoticz.')

api.add_namespace(ping_namespace, path='/ping')
api.add_namespace(auth_namespace, path='/auth')