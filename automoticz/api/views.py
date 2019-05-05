from flask import Blueprint
from flask import redirect
from flask_restplus import Api
from google.auth import exceptions
from oauthlib.oauth2.rfc6749 import errors

from automoticz.utils.constants import MESSAGE
from automoticz.api.endpoints import *

from automoticz.extensions import jwt
from automoticz.utils import is_token_revoked

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    api_blueprint,
    title='Automoticz API',
    version='1.0-dev',
    description='REST API for Automoticz system.')

api.add_namespace(system_namespace, path='/system')
api.add_namespace(beacon_auth_namespace, path='/beacon_auth')
api.add_namespace(oauth_namespace, path='/oauth2')


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


# Handling errors
@api.errorhandler(exceptions.RefreshError)
def proximity_api_is_not_initialized(error):
    return {'message': MESSAGE.API_NOT_INITIALIZED}, 500


@api.errorhandler(exceptions.DefaultCredentialsError)
def no_credentials_provided(error):
    return {'message': MESSAGE.NO_CREDENTIALS_PROVIDED}, 500


@api.errorhandler(errors.InvalidGrantError)
def invalid_grant_error(error):
    return redirect(url_for('oauth2.authorize'))