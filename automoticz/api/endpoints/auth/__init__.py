from flask_restplus import Namespace

auth_namespace = Namespace(
    'auth', description='Auth endpoint for server authentication.')

from .routes import *

__all__ = ['auth_namespace']
