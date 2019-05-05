from flask import Blueprint

from flask_restplus import Namespace
from oauthlib.oauth2.rfc6749 import errors

namespace = Namespace(
    'oauth2', description='Google OAuth2 endpoint.')

from .routes import *

# Handling errors
@namespace.errorhandler(errors.InvalidGrantError)
def invalid_grant_error(error):
    return redirect(url_for('api.oauth2_authorize'))

__all__ = ['namespace']