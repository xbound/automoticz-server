import time

from flask_jwt_extended import jwt_required
from flask_restplus import Resource, fields

from automoticz.extensions import proximity
from automoticz.models import OAuth2Credentials
from automoticz.utils.constants import RESPONSE_MESSAGE
from automoticz.utils.home import get_users
from automoticz.utils.rest import response_base
from automoticz.utils import errors
from automoticz.tasks import *
from automoticz.utils.oauth2 import get_default_credentials
from automoticz.utils.wsdevices import *

from . import namespace
from .helpers import WSDevice_model, wsdevice_list_response

systime_response = namespace.model(
    'System time  response', {
        'time':
        fields.String(description='Server time',
                      example='Monday March, 04 2019 20:55:33'),
    })

execute_command_reponse = namespace.model('Execute command response',
                                          response_base)


@namespace.route('/ping')
class Ping(Resource):
    '''
    Ping endpoint.
    '''

    def get(self):
        return {'status': 'OK'}, 200


@namespace.route('/activate')
class Activate(Resource):
    '''
    Proximity Beacon API initialization endpoint.
    '''

    def get(self):
        if not proximity.api:
            creds = get_default_credentials()
            proximity.init_api(creds)
        return {}, 200


@namespace.route('/systime')
class SysTime(Resource):
    '''
    System time endpoint
    '''

    @jwt_required
    @namespace.marshal_with(systime_response)
    def get(self):
        return {'time': time.strftime('%A %B, %d %Y %H:%M:%S')}, 200


@namespace.route('/ws_devices')
class WSDeviceList(Resource):
    '''
    Websocket device list endpoint.
    '''

    @jwt_required
    @namespace.marshal_with(wsdevice_list_response)
    def get(self):
        devices = get_ws_devices()
        return {
            'code': 'WSDEVICES',
            'message': 'Wsdevices',
            'wsdevices': devices,
        }, 200


@namespace.route('/ws_devices/<int:device_id>')
@namespace.header('Authorization', description='Auth header')
class WSDeviceDetails(Resource):
    '''
    Websocket device details endpoint.
    '''

    @jwt_required
    @namespace.marshal_with(WSDevice_model)
    def get(self, device_id):
        return get_ws_device_details(device_id)


@namespace.route(
    '/ws_devices/<int:device_id>/commands/<int:command_id>/execute')
@namespace.header('Authorization', description='Auth header')
class WSCommandExecute(Resource):
    '''
    Websocket device details endpoint.
    '''

    @jwt_required
    @namespace.marshal_with(execute_command_reponse)
    def get(self, device_id, command_id):
        device_id = int(device_id)
        command_id = int(command_id)
        if not is_device_online(device_id):
            raise errors.DeviceNotOnline()
        command = wsdevices.get_device_command(device_id, command_id)
        if command is None:
            return {
                'code': 'COMMAND',
                'message': 'Command sent for execution',
            }, 200
        event = command.event
        socketio.emit(event, command.json_command)
        return {
            'code': 'COMMAND',
            'message': 'Command sent for execution',
        }, 200
