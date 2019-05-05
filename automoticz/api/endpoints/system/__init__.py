from flask_restplus import Namespace

system_namespace = Namespace(
    'system', description='Endpoint group for calling common system functions.')

from .routes import *

__all__ = ['system_namespace']
