import itertools
from datetime import datetime

from dateutil import parser
from flask import current_app as app

from automoticz.models import ws_devices
from automoticz.extensions import cache, celery_app, db, socketio
from automoticz.utils import beacons, constants, tool, wsdevices, home


@celery_app.task(bind=True)
def get_default_auth_beacon(self):
    beacon = beacons.get_default_auth_beacon_name()
    cache.set('beacon_name', beacon)


@celery_app.task(bind=True)
def get_beacon_pin(self):
    beacons.get_pin()


@celery_app.task(bind=True)
def set_beacon_pin(self):
    pin = beacons.generate_pin()
    pin_str = tool.to_json(pin)
    resp = beacons.set_pin(pin_str)
    # Veryfing response
    if resp.get('data') == tool.str_to_base64(pin_str):
        cache.set(constants.CACHE_PIN_KEY, pin[constants.PIN_ATTACHMENT_KEY])
        cache.set(constants.CACHE_SET_PIN_KEY,
                  pin,
                  timeout=constants.CACHE_SET_PIN_KEY_TIMEOUT)


@celery_app.task(bind=True)
def ws_device_send_command(self, device_id, command_id):
    command = wsdevices.get_device_command(device_id, command_id)
    if command is None:
        return
    event = command.event
    socketio.emit(event, command.json_command)


@celery_app.task(bind=True)
def ws_device_register_domoticz(self, device_id):
    device = ws_devices.WSDevice.query.get(device_id)
    if device:
        wsdevices.register_ws_device_domoticz(device)
