from flask_restplus import Namespace

namespace = Namespace(
    'system', description='Endpoint group for calling common system functions.')

from .routes import *

__all__ = ['namespace']
