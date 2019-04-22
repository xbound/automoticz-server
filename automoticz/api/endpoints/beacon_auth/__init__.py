from flask_restplus import Namespace

beacon_auth_namespace = Namespace(
    'beacon_auth', description='Endpoint for registering device and registering user presence.')

from .routes import *

__all__ = ['beacon_auth_namespace']
