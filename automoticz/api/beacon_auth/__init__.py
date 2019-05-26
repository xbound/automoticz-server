from flask_restplus import Namespace

from google.auth import exceptions
from automoticz.utils import errors
from automoticz.utils.constants import RESPONSE_MESSAGE
import binascii

namespace = Namespace(
    'beacon_auth',
    description='Endpoint for registering device and registering user presence.'
)

from .routes import *


# Handling errors
@namespace.errorhandler(exceptions.RefreshError)
def proximity_api_is_not_initialized(error):
    return make_error_response(error,
                               message=RESPONSE_MESSAGE.API_NOT_INITIALIZED,
                               http_code=500)


@namespace.errorhandler(exceptions.DefaultCredentialsError)
def no_credentials_provided(error):
    return make_error_response(
        error, message=RESPONSE_MESSAGE.NO_CREDENTIALS_PROVIDED, http_code=500)


@namespace.errorhandler(errors.InvalidDomoticzLoginCredentilas)
def invalid_domoticz_login_credentials(error):
    return errors.make_error_response(error)


@namespace.errorhandler(errors.InvalidPin)
def invalid_pin(error):
    return errors.make_error_response(error)


# @namespace.errorhandler(binascii.Error)
# def incorect_padding(error: binascii.Error):
#     return {'message': 'Wrong base64 value'}, 400

__all__ = ['namespace']
