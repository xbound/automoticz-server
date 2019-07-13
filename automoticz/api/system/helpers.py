from flask_restplus import fields

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
        'id': fields.String(description='Command ID'),
    })

WSState_model = api.model(
    'WS State model', {
        'value': fields.String(description='State value'),
        'description': fields.String(description='State description'),
        'name': fields.String(description='State name'),
        'id': fields.String(description='State ID'),
    })

WSDevice_list_item = api.model(
    'WS Device list item', {
        'id': rest.wsdevice_id_field,
        'name': rest.wsdevice_name_field,
        'description': rest.wsdevice_description_field,
        'is_online': rest.wsdevice_is_online_field,
    })

WSDevice_model = api.model(
    'WS Device model',
    {
        'id':
        rest.wsdevice_id_field,
        'name':
        rest.wsdevice_name_field,
        'description':
        rest.wsdevice_description_field,
        'machine':
        rest.wsdevice_machine_filed,
        'sysname':
        rest.wsdevice_sysname_field,
        'device_type':
        rest.wsdevice_device_type_field,
        'states':
        fields.List(fields.Nested(WSState_model), description='States'),
        'is_online':
        rest.wsdevice_is_online_field,
        'commands':
        fields.List(fields.Nested(WSCommand_model), description='Commands'),
        'version':
        rest.wsdevice_version_field,
    },
)

wsdevice_list_response = api.inherit(
    'WS devices GET response', base_model, {
        'wsdevices':
        fields.List(fields.Nested(WSDevice_list_item), description='Commands'),
    })
