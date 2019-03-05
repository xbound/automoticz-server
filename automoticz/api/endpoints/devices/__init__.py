from flask_restplus import Namespace

devices_namespace = Namespace(
    'devices', description='Endpoint for interaction with bluetooth devices.')

from .routes import *

__all__ = ['devices_namespace']
