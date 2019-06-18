from flask_restplus import fields

from automoticz.utils.constants import RESPONSE_MESSAGE
from automoticz.utils import rest
from . import namespace as api

wsdevices_reguest = api.model('WS devices GET request', {
    'access_token': rest.access_token_field,
})

base_model = api.model('WS Device GET base response', rest.response_base)

WSCommand_model = api.model(
    'WS Command model', {
        'description': fields.String(description='Command description'),
        'name': fields.String(description='Command name'),
        'command_id': fields.String(description='Command ID'),
    })

WSDevice_model = api.model(
    'WS Device model',
    {
        'name':
        fields.String(description='WebSocket device name'),
        'machine':
        fields.String(description='WebSocket device machine'),
        'sysname':
        fields.String(description='WebSocket device version'),
        'device_type':
        fields.String(description='WebSocket device type'),
        'state':
        fields.String(description='WebSocket device state'),
        'is_online':
        fields.Boolean(description='Websocket device connection status'),
        'commands':
        fields.List(fields.Nested(WSCommand_model), description='Commands'),
    },
)

wsdevice_response = api.inherit(
    'WS devices GET response', base_model, {
        'wsdevices':
        fields.List(fields.Nested(WSDevice_model), description='Commands'),
    })
