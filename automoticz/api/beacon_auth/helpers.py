from flask_restplus import fields

from automoticz.utils.constants import RESPONSE_MESSAGE
from automoticz.utils import rest
from . import namespace as api

# Fields
access_token_field = fields.String(
    description='Access token',
    example=
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwiZnJlc2giOmZhbHNlLCJleHAiOjE1NTY0NzM4MzYsIm5iZiI6MTU1NjQ3MjkzNiwiaWRlbnRpdHkiOjUsImp0aSI6ImE4OTI1Mzk1LWQyM2QtNGRmNC04MDZlLWNhMWRiMGVhNTgzOSIsImlhdCI6MTU1NjQ3MjkzNn0.HhWTa70hnAtyf6WzoT8hBj_4WTo2nYjVBvlJGHREqEk'
)
refresh_token_field = fields.String(
    description='Refresh token',
    example=
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6NSwidHlwZSI6InJlZnJlc2giLCJuYmYiOjE1NTY0NzI5MzYsImp0aSI6IjU4OTNhYTI2LWM2YTYtNGM1MC1iZmIzLWM5MjA4NGNhNTcxNCIsImlhdCI6MTU1NjQ3MjkzNn0.Rown-44Zg1kpAnXKubTWwGaDER4deqW2PdqQLTmTTs0'
)

# Models

# Login models
register_reguest = api.model(
    'Device registration request', {
        'pin':
        rest.Base64String(description='Base64 encoded token', required=True),
        'client':
        fields.String(description='Client name'),
        'client_uuid':
        fields.String(description='Client UUID (unique identifier)', required=True),
        'login':
        fields.String(description='Domoticz user login', required=True),
        'password':
        rest.Base64String(description='Domoticz user password', required=True),
    })

register_response = api.model(
    'Device registration  response', {
        'message':
        fields.String(description='Response message', example=RESPONSE_MESSAGE.LOGIN),
        'access_token':
        access_token_field,
        # 'refresh_token':
        # refresh_token_field,
    })

# Token refresh models
token_refresh_request = api.model('Token refresh request',
                                  {'refresh_token': refresh_token_field})

token_refresh_response = api.model(
    'Device token refresh response', {
        'message':
        fields.String(description='Response message', example=RESPONSE_MESSAGE.REFRESH),
        'access_token':
        access_token_field
    })

# Revoke access models
revoke_access_request = api.model('Revoke access request',
                                  {'access_token': access_token_field})

revoke_access_response = api.model(
    'Device revoke access response', {
        'message':
        fields.String(description='Response message',
                      example=RESPONSE_MESSAGE.REVOKE_ACCESS)
    })

# Revoke refresh models
revoke_refresh_request = api.model('Revoke refresh request',
                                   {'refresh_token': refresh_token_field})

revoke_refresh_response = api.model(
    'Device revoke refresh response', {
        'message':
        fields.String(description='Response message',
                      example=RESPONSE_MESSAGE.REVOKE_REFRESH),
    })
