from flask import current_app as app
from flask_restplus import Namespace

from jwt.exceptions import ExpiredSignatureError
from google.auth import exceptions
from automoticz.utils import errors
from automoticz.utils.constants import RESPONSE_MESSAGE
import binascii

namespace = Namespace(
    'beacon_auth',
    description='Endpoint for registering device and registering user presence.'
)

from .routes import *

from automoticz.extensions import jwt
from automoticz.utils.auth import is_token_revoked


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


# Handling errors
@namespace.errorhandler(exceptions.RefreshError)
def proximity_api_is_not_initialized(error):
    return errors.make_error_response(
        error, message=RESPONSE_MESSAGE.API_NOT_INITIALIZED, http_code=500)


@namespace.errorhandler(exceptions.DefaultCredentialsError)
def no_credentials_provided(error):
    return errors.make_error_response(
        error, message=RESPONSE_MESSAGE.NO_CREDENTIALS_PROVIDED, http_code=500)


@namespace.errorhandler(errors.InvalidDomoticzLoginCredentilas)
def invalid_domoticz_login_credentials(error):
    return errors.make_error_response(error)


@namespace.errorhandler(errors.AutomoticzError)
def automoticz_error(error):
    return errors.make_error_response(error)



@namespace.errorhandler(ExpiredSignatureError)
def jwt_token_expired(error):
    return errors.make_error_response(error,
                                      code=RESPONSE_CODE.EXPIRED_TOKEN,
                                      message=RESPONSE_MESSAGE.EXPIRED_TOKEN,
                                      http_code=401)


# @namespace.errorhandler(binascii.Error)
# def incorect_padding(error: binascii.Error):
#     return {'message': 'Wrong base64 value'}, 400

__all__ = ['namespace']
