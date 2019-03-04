from flask import Blueprint
from flask_restplus import Api
from google.auth import exceptions

from automoticz.utils.constants import MESSAGE
from automoticz.api.endpoints import *

oauth2_blueprint = Blueprint('oauth2', __name__, url_prefix='/oauth2')

from automoticz.api.oauth2 import *

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    api_blueprint,
    title='Automoticz API',
    version='1.0-dev',
    description='REST API for automoticz.')

api.add_namespace(maintanance_namespace, path='/maintanance')
api.add_namespace(auth_namespace, path='/auth')

# Handling errors
@api.errorhandler(exceptions.RefreshError)
def proximity_api_is_not_initialized(error):
    return {'message': MESSAGE.API_NOT_INITIALIZED}, 500


@api.errorhandler(exceptions.DefaultCredentialsError)
def no_credentials_provided(error):
    return {'message': MESSAGE.NO_CREDENTIALS_PROVIDED}, 500