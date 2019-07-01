import socketio
import random

CONFIG_DATA = {
    "Server": "http://192.168.0.108:5000/",
    "DeviceInfo": {
        "name": "ESP-32-{:03d}".format(random.randint(0, 99)),
        "description": "Simple switch",
        "machine": 'ESP32-SIM',
        "sysname": "ESP32-micropython",
        "version": "v1.0",
        "type": "switch",
    },
    "Commands": [
        {
            "type": "INFO",
            "description": "Device info",
            "event": "message",
            "name": "GET_INFO"
        },
        {
            "type": "MOD",
            "value": "On",
            "description": "Device state on",
            "event": "message",
            "name": "TURN_ON"
        },
        {
            "type": "MOD",
            "value": "Off",
            "description": "Device state off",
            "name": "TURN_OFF"
        }
    ]
}

DEVICE_INFO = {
    'name': CONFIG_DATA['DeviceInfo']['name'],
    'description': CONFIG_DATA['DeviceInfo']['description'],
    'type': CONFIG_DATA['DeviceInfo']['type'],
    'machine': CONFIG_DATA['DeviceInfo']['machine'],
    'sysname': CONFIG_DATA['DeviceInfo']['sysname'],
    'version': CONFIG_DATA['DeviceInfo']['version'],
    'state': random.choice([True, False]),
    'commands': CONFIG_DATA['Commands']
}

def _get_standard_msg_body(message='OK'):
    return {
        'message': message,
        'type': CONFIG_DATA['DeviceInfo']['type'],
    }

def get_mod_resp(msg):
    VALUE_MAP = {
        'On': True,
        'Off': False,
        '1': True,
        '0': False
    }
    msg_value = msg.get('value')
    if not msg_value:
        return get_error_resp(
            msg, 'No value set'
        )
    value_ = VALUE_MAP.get(msg_value)
    if value_ is None:
        return get_error_resp(
            msg, 'Bad value {}'.format(msg_value)
        )
    resp = _get_standard_msg_body('MOD')
    resp['state'] = value_
    return resp


def get_error_resp(msg, cause=None):
    error_resp = {
        'message': 'ERROR',
        'description': 'Bad type'
    }
    if cause:
        error_resp['description'] = cause
    return error_resp


def get_info_resp(msg=None):
    resp = _get_standard_msg_body('INFO')
    resp.update(**DEVICE_INFO)
    return resp

MSG_MAP = {
    'INFO': get_info_resp,
    'MOD': get_mod_resp
}



sio = socketio.Client()

@sio.event
def message(data):
    msg_type = data.get('type')
    resp_func = MSG_MAP.get(msg_type, get_error_resp)
    resp = resp_func(data)
    print("Response: {}".format(resp))
    sio.emit('message', resp)


if __name__ == "__main__":
    print('Connecting to server...')
    sio.connect(CONFIG_DATA['Server'])
    print('Sending registeration data...')
    sio.emit('device_register', get_info_resp())
    sio.wait()