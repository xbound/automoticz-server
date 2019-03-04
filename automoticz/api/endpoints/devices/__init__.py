from flask_restplus import Namespace

devices_namespace = Namespace(
    'auth', description='Auth endpoint for server authentication.')

from .routes import *

__all__ = ['devices_namespace']
