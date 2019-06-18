from flask_restplus import fields

from automoticz.utils.constants import RESPONSE_MESSAGE
from automoticz.utils import rest
from . import namespace as api

# Models

# Login models
register_reguest = api.model(
    'Login POST request', {
        'pin':
        rest.Base64String(description='Base64 encoded token', required=True),
        'client':
        fields.String(description='Client name'),
        'client_uuid':
        fields.String(description='Client UUID (unique identifier)',
                      required=True),
        'login':
        fields.String(description='Domoticz user login', required=True),
        'password':
        rest.Base64String(description='Domoticz user password', required=True),
    })

base_model = api.model('Base model', rest.response_base)

register_response = api.inherit('Login POST response', base_model, {
    'access_token': rest.access_token_field,
})
