from flask import request, session
from flask_socketio import send, emit
from flask_jwt_extended import jwt_required

from automoticz.extensions import socketio
from automoticz.utils.wsdevices import *


@socketio.on('on_data')
def on_data(data):
    emit('alert', {'a': 1}, room=request.sid)
    return True


@socketio.on('message')
def on_message(data):
    device_sid = request.sid
    device = get_ws_device(device_sid, data)
    if not device:
        return
    if data.get('message') == 'OK':
        update_wsdevice_data(device, data)
        emit('subscribers_notify',
             device.to_dict(),
             broadcast=True,
             include_self=False)


@socketio.on('device_register')
def on_device_register(data):
    device_sid = request.sid
    is_new = register_ws_device(device_sid, data)
