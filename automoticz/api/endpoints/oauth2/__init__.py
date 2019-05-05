from flask import Blueprint

from flask_restplus import Namespace

oauth_namespace = Namespace(
    'oauth2', description='Google OAuth2 endpoint.')

from .routes import *

__all__ = ['oauth_namespace']