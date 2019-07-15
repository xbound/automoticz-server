import pprint

from flask import request, session
from flask_jwt_extended import jwt_required
from flask_socketio import emit, send, join_room, leave_room

from automoticz.extensions import get_logger, socketio
from automoticz.utils.tool import *
from automoticz.utils.wsdevices import *
from automoticz.utils.wssubcribers import *

from automoticz.tasks import ws_device_register_domoticz


def log_data(data):
    pretty_log_info('Data recived:\n{}', data)


@socketio.on('on_data')
def on_data(data):
    emit('alert', {'a': 1}, room=request.sid)
    return True


@socketio.on('connect')
def on_connect():
    device_sid = request.sid
    log.info('Connected with sid: {}'.format(device_sid))


@socketio.on('disconnect')
def on_discconect():
    sid = request.sid
    log.info('Disconnected with sid: {}'.format(sid))
    device = unregister_device(sid)
    if not device:
        unregister_subsriber(sid)
    else:
        emit('device_updated',
             get_ws_device_json(device),
             room='subscribers',
             broadcast=True,
             include_self=False)


@socketio.on('device_update')
def on_device_update(data):
    log_data(data)
    device_sid = request.sid
    if isinstance(data, str):
        data = str_to_json(data)
    device = get_ws_device(device_sid, data)
    if not device:
        return
    was_updated = update_wsdevice_data(device, data)
    ws_device_register_domoticz.delay(device.id)
    if was_updated:
        emit('device_updated',
             get_ws_device(device_sid, data, as_json=True),
             room='subscribers',
             broadcast=True,
             include_self=False)


@socketio.on('device_register')
def on_device_register(data):
    log_data(data)
    device_sid = request.sid
    device = register_ws_device(device_sid, data)
    ws_device_register_domoticz.delay(device.id)
    if device:
        log.info('Device registered: {}'.format(str(data)))
    else:
        log.info('Device re-register: {}'.format(str(data)))
    emit('device_updated',
         get_ws_device(device_sid, data, as_json=True),
         room='subscribers',
         broadcast=True,
         include_self=False)
    return True


@socketio.on('subscriber_register')
def on_subscriber_register(data):
    log_data(data)
    subscriber_sid = request.sid
    if isinstance(data, str):
        data = str_to_json(data)
    is_new = register_subscriber(subscriber_sid, data)
    if is_new:
        join_room('subscribers')
        log.info('Subscriber registered: {}'.format(str(data)))
    return True
