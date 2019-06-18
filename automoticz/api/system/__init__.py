from flask_restplus import Namespace

from automoticz.utils.errors import make_error_response

namespace = Namespace(
    'system', description='Endpoint group for calling common system functions.')

from .routes import *

__all__ = ['namespace']

from flask_jwt_extended import exceptions

@namespace.errorhandler(exceptions.NoAuthorizationError)
def no_authorization_token_provided(error):
    return make_error_response(error,
                               message=RESPONSE_MESSAGE.API_NOT_INITIALIZED,
                               http_code=500)