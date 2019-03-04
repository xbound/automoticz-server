from flask_restplus import Namespace

maintanance_namespace = Namespace(
    'maintanance', description='Endpoint for server common maintanance.')

from .routes import *

__all__ = ['maintanance_namespace']
