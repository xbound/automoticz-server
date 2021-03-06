import uos
import utime
import machine
import random

import device

import usocketio.client

timer = machine.Timer(-1)
led = machine.Pin(2, machine.Pin.OUT)

VALUE_MAPPING = {
    True: 'On',
    False: 'Off',
    1: 'On',
    0: 'Off',
    'On': True,
    'Off': False,
    '1': True,
    '0': False
}

DEVICE_INFO = {
    'name':
    device.CONFIG_DATA['DeviceInfo']['name'],
    'description':
    device.CONFIG_DATA['DeviceInfo']['description'],
    'type':
    device.CONFIG_DATA['DeviceInfo']['type'],
    'machine':
    uos.uname().machine,
    'sysname':
    uos.uname().sysname,
    'version':
    uos.uname().version,
    'states': [
        {
            'name': 'LED',
            'description': 'State of built-in LED',
            'value': VALUE_MAPPING[led.value()],
            'state_type': 'switch',
        },
    ],
    'commands':
    device.CONFIG_DATA['Commands']
}


def _get_standard_msg_body(message='OK'):
    return {
        'message': message,
        'type': device.CONFIG_DATA['DeviceInfo']['type'],
    }


def get_mod_resp(msg):
    msg_value = msg.get('value')
    if not msg_value:
        return get_error_resp(msg, 'No value set')
    value_ = VALUE_MAPPING.get(msg_value)
    if value_ is None:
        return get_error_resp(msg, 'Bad value {}'.format(msg_value))
    led.value(value_)
    resp = _get_standard_msg_body('MOD')
    resp['states'] = [{
        'name': 'LED',
        'description': 'State of built-in LED',
        'value': VALUE_MAPPING[led.value()],
        'state_type': 'switch',
    }]
    return resp


def get_error_resp(msg, cause=None):
    error_resp = {'message': 'ERROR', 'description': 'Bad type'}
    if cause:
        error_resp['description'] = cause
    return error_resp


def get_info_resp(msg=None):
    resp = _get_standard_msg_body('INFO')
    resp.update(**DEVICE_INFO)
    return resp


MSG_MAP = {'INFO': get_info_resp, 'MOD': get_mod_resp}


def device_start():
    try:
        with usocketio.client.connect(server_url) as socketio:

            @socketio.on('message')
            def on_message(message):
                msg_type = message.get('type')
                print('Incoming message: {}'.format(message))
                resp_func = MSG_MAP.get(msg_type, get_error_resp)
                resp = resp_func(message)
                print("Response: {}".format(resp))
                socketio.emit('device_update', resp)

            def one_shot(t):
                socketio.emit('device_register', get_info_resp())
                # timer.init(mode=machine.Timer.PERIODIC,
                #            period=15000,
                #            callback=periodic_task)

            def periodic_task(t):
                led.value(not led.value())
                resp = _get_standard_msg_body('UPD')
                resp['name'] = DEVICE_INFO['name']
                resp['states'] = [
                    {
                        'name': 'LED',
                        'value': VALUE_MAPPING[led.value()],
                    },
                ]
                socketio.emit('device_update', resp)

            timer.init(mode=machine.Timer.ONE_SHOT,
                       period=3000,
                       callback=lambda t: one_shot(t))
            socketio.run_forever()
    except Exception as e:
        print("Error: ", e)
        utime.sleep(5)
        print('Reconnecting...')
        device_start()


server_url = device.CONFIG_DATA['Server']
device_start()
