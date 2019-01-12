from flask_restplus import fields

from automoticz.commons.constants import MESSAGE
from automoticz.api.endpoints.auth import auth_namespace as api

# Fields
username_field = fields.String(
    required=True, description='Username', example='your_username')
access_token_field = fields.String(
    description='Access token', example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9')
refresh_token_field = fields.String(
    description='Refresh token', example='IkpXVCJ9.eyJpZGVudGl0eSI6InlvdX')

# Models

# Login models
login_reguest = api.model(
    'Auth request', {
        'username':
        username_field,
        'blu_id':
        fields.String(
            required=True,
            description='Device bluetooth address',
            example='91:74:4D:78:FC:30')
    })

login_response = api.model(
    'Auth response', {
        'message':
        fields.String(description='Response message', example=MESSAGE.LOGIN),
        'access_token':
        access_token_field,
        'refresh_token':
        refresh_token_field
    })

# Token refresh models
token_refresh_request = api.model('Token refresh request',
                                  {'refresh_token': refresh_token_field})

token_refresh_response = api.model(
    'Token refresh response', {
        'message':
        fields.String(description='Response message', example=MESSAGE.REFRESH),
        'access_token':
        access_token_field
    })

# Revoke access models
revoke_access_request = api.model('Revoke access request',
                                  {'access_token': access_token_field})

revoke_access_response = api.model(
    'Revoke access response', {
        'message':
        fields.String(
            description='Response message', example=MESSAGE.REVOKE_ACCESS),
        'username':
        username_field
    })

# Revoke refresh models
revoke_refresh_request = api.model('Revoke refresh request',
                                   {'refresh_token': refresh_token_field})

revoke_refresh_response = api.model(
    'Revoke refresh response', {
        'message':
        fields.String(
            description='Response message', example=MESSAGE.REVOKE_REFRESH),
        'username':
        username_field
    })
