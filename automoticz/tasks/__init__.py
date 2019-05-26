from datetime import datetime
from dateutil import parser
import itertools

from flask import current_app as app

from automoticz.extensions import celery_app, db, cache
from automoticz.utils import constants
from automoticz.utils import to_json, str_to_base64, get_pin, generate_pin, set_pin
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
