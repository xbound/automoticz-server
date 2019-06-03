from datetime import datetime
from dateutil import parser
import itertools

from flask import current_app as app

from automoticz.extensions import celery_app, db, cache, wsmanager
from automoticz.utils import constants
from automoticz.utils import to_json, to_dict, str_to_base64, get_pin, generate_pin, set_pin
from automoticz.utils import get_default_auth_beacon_name


@celery_app.task(bind=True)
def get_default_auth_beacon(self):
    beacon = get_default_auth_beacon_name()
    cache.set('beacon_name', beacon)


@celery_app.task(bind=True)
def get_beacon_pin(self):
    get_pin()


@celery_app.task(bind=True)
def set_beacon_pin(self):
    pin = generate_pin()
    pin_str = to_json(pin)
    resp = set_pin(pin_str)
    # Veryfing response
    if resp.get('data') == str_to_base64(pin_str):
        cache.set(constants.CACHE_PIN_KEY, pin[constants.PIN_ATTACHMENT_KEY])
        cache.set(constants.CACHE_SET_PIN_KEY,
                  pin,
                  timeout=constants.CACHE_SET_PIN_KEY_TIMEOUT)


@celery_app.task(bind=True)
def ws_device_send(self, device_name, query_name):
    ws = wsmanager.get_device(device_name)
    ws.send_query(query_name)

@celery_app.task(bind=True)
def ws_get_info_drom_devices(self):
    for key, wswrapper in wsmanager.get_devices().items():
        wsdevice = wsmanager.get_device_db_instance(key)
        res = wswrapper.send_query('DEVICE_INFO')
        res = to_dict(res)
        print(wsdevice)
        wsdevice.machine = res['machine']
        wsdevice.sysname = res['sysname']
        wsdevice.version = res['version']
        wsdevice.status = res['status']
        wsdevice.device_type = res['type']
        db.session.commit()