import json
import uuid

from tests.helpers import json_response, post_json, to_base64, delete_json, get_json

from automoticz.models import ws_devices
from automoticz.utils import constants
from automoticz.utils.beacons import get_pin

params = {
    'commands': [{
        'description': 'Device info',
        'event': 'message',
        'name': 'GET_INFO',
        'type': 'INFO'
    }, {
        'description': 'Device state on',
        'event': 'message',
        'name': 'TURN_ON',
        'type': 'MOD',
        'value': 'On'
    }, {
        'description': 'Device state off',
        'name': 'TURN_OFF',
        'type': 'MOD',
        'value': 'Off'
    }],
    'description':
    'Simple switch',
    'machine':
    'ESP32-SIM',
    'message':
    'INFO',
    'name':
    'ESP-32-test',
    'states': [{
        'description': 'State of built-in LED',
        'name': 'LED',
        'value': 'False'
    }],
    'sysname':
    'ESP32-micropython',
    'type':
    'switch',
    'version':
    'v1.0'
}


def test_ws_device_register(app, database, sio):

    client = sio.test_client(app)
    client.get_received()
    client.emit('device_register', params)
    with app.app_context():
        devices = ws_devices.WSDevice.query.all()
        commands = ws_devices.WSCommand.query.all()
        states = ws_devices.WSState.query.all()
        assert len(commands) == 3
        assert len(devices) == 1
        assert len(states) == 1

    client.disconnect()


def test_ws_device_update(app, database, sio):
    client = sio.test_client(app)
    client.get_received()
    client.emit('device_register', params)
    with app.app_context():
        device = ws_devices.WSDevice.query.all()[0]
        dict1 = device.to_dict()
    params['machine'] = 'eps32_12F'
    params['commands'][0]['description'] = 'Test'
    params['states'].append({
        'description': 'sfgdhg',
        'name': 'LED#2',
        'value': 'Off'
    })
    client.emit('device_update', params)
    with app.app_context():
        device = ws_devices.WSDevice.query.all()[0]
        dict2 = device.to_dict()
    assert dict1 != dict2
    assert len(dict1['states']) < len(dict2['states'])
    client.disconnect()


def test_ws_device_update_2(app, database, sio):
    client = sio.test_client(app)
    client.get_received()
    client.emit('device_register', params)
    with app.app_context():
        device = ws_devices.WSDevice.query.all()[0]
        dict1 = device.to_dict()
    client.emit(
        'device_update', {
            'message': 'MOD',
            'states': {
                'description': 'State of built-in LED',
                'name': 'LED',
                'value': 'Off'
            },
            'type': 'switch'
        })
    with app.app_context():
        device = ws_devices.WSDevice.query.all()[0]
        dict2 = device.to_dict()
    assert dict1 != dict2
    client.disconnect()


def test_ws_subsciber_register(app, database, client, sio):
    uuid = '40ad6536-a5a4-11e9-8474-70188b8d1ef7'
    expired_access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE1NjMwNDczODcsImlkZW50aXR5IjoiNDBhZDY1MzYtYTVhNC0xMWU5LTg0NzQtNzAxODhiOGQxZWY3IiwiaWF0IjoxNTYzMDQ3Mzg3LCJqdGkiOiJkZDJkOTczOS1lYTg2LTRmZGMtYTI2MC1mNDc4ZDNiYTg5ZmYiLCJleHAiOjE1NjMwNDc2ODcsInR5cGUiOiJhY2Nlc3MiLCJmcmVzaCI6ZmFsc2V9.eeeKjKOaJAjjIvo70wDwEMHf4rMdpdpiz4lm9ujQ2pg'
    domoticz_login = app.config.DOMOTICZ_USERNAME
    domoticz_password = to_base64(str(app.config.DOMOTICZ_PASSWORD))
    with app.app_context():
        valid_pin = to_base64(get_pin())
    json_payload = {
        'pin': valid_pin,
        'client': 'Android Google Pixel 3',
        'client_uuid': uuid,
        'login': domoticz_login,
        'password': domoticz_password
    }
    response = post_json(client, 'api/beacon_auth/login', json_payload)
    response_json = json_response(response)
    access_token = response_json['access_token']
    sio_client = sio.test_client(app)
    sio_client.get_received()
    sio_client.emit('subscriber_register', {
        'client_uuid': uuid,
    })