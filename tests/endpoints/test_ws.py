from automoticz.models import ws_devices


def test_ws_device_register(app, database, sio):

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
