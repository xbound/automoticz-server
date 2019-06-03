from flask import request
from flask_socketio import send, emit
from automoticz.extensions import socketio

sids = []

@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    if sid in sids:
        sids.remove(sid)
    return True
    
@socketio.on('device_register')
def on_device_register(data):
    sid = request.sid

    
@socketio.on('message')
def on_message(data):
    return True