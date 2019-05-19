from flask_restplus import Namespace

from google.auth import exceptions
from automoticz.utils import errors
from automoticz.utils.constants import MESSAGE

namespace = Namespace(
    'beacon_auth',
    description='Endpoint for registering device and registering user presence.'
)

from .routes import *


# Handling errors
@namespace.errorhandler(exceptions.RefreshError)
def proximity_api_is_not_initialized(error):
    return {'message': MESSAGE.API_NOT_INITIALIZED}, 500


@namespace.errorhandler(exceptions.DefaultCredentialsError)
def no_credentials_provided(error):
    return {'message': MESSAGE.NO_CREDENTIALS_PROVIDED}, 500


@namespace.errorhandler(errors.InvalidDomoticzLoginCredentilas)
def invalid_domoticz_login_credentials(error):
    return {'message': MESSAGE.INVALID_CREDS}, 400


__all__ = ['namespace']
