from flask_restplus import fields

from automoticz.utils.constants import MESSAGE
from . import beacon_auth_namespace as api

# Fields
access_token_field = fields.String(
    description='Access token', example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9')
refresh_token_field = fields.String(
    description='Refresh token', example='IkpXVCJ9.eyJpZGVudGl0eSI6InlvdX')

# Models

# Login models
register_reguest = api.model(
    'Device registration request', {
        'pin': fields.String(description='Base64 encoded token'),
        'client': fields.String(description='Client name'),
    })

register_response = api.model(
    'Device registration  response', {
        'message':
        fields.String(description='Response message', example=MESSAGE.LOGIN),
        'access_token':
        access_token_field
    })

# Token refresh models
token_refresh_request = api.model('Token refresh request',
                                  {'refresh_token': refresh_token_field})

token_refresh_response = api.model(
    'Device token refresh response', {
        'message':
        fields.String(description='Response message', example=MESSAGE.REFRESH),
        'access_token':
        access_token_field
    })

# Revoke access models
revoke_access_request = api.model('Revoke access request',
                                  {'access_token': access_token_field})

revoke_access_response = api.model(
    'Device revoke access response', {
        'message':
        fields.String(
            description='Response message', example=MESSAGE.REVOKE_ACCESS)
    })

# Revoke refresh models
revoke_refresh_request = api.model('Revoke refresh request',
                                   {'refresh_token': refresh_token_field})

revoke_refresh_response = api.model(
    'Device revoke refresh response', {
        'message':
        fields.String(
            description='Response message', example=MESSAGE.REVOKE_REFRESH),
    })
