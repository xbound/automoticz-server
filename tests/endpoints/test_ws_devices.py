import json
import uuid

from tests.helpers import get_json, json_response, post_json, to_base64

from automoticz.utils import constants
from automoticz.utils.beacons import get_pin


def test_ws_devices(app, client):
    domoticz_login = app.config.DOMOTICZ_USERNAME
    domoticz_password = to_base64(str(app.config.DOMOTICZ_PASSWORD))
    domoticz_password_invalid = to_base64('1234')

    with app.app_context():
        valid_pin = to_base64(get_pin())
    json_payload = {
        'pin': valid_pin,
        'client': 'Android Google Pixel 3',
        'client_uuid': str(uuid.uuid1()),
        'login': domoticz_login,
        'password': domoticz_password
    }
    response = post_json(client, 'api/beacon_auth/login', json_payload)
    response_json = json_response(response)
    assert response.status_code == 200
    assert 'access_token' in response_json
    access_token = response_json['access_token']

    json_payload = {'access_token': access_token}
    response = get_json(client, 'api/system/ws_devices', headers={
        'Authorization': 'Bearer {}'.format(access_token)
    })
    assert response.status_code == 200
    response_json = json_response(response)
    assert response_json
    assert type(response_json['wsdevices']) == list


def test_ws_details(app, client):
    domoticz_login = app.config.DOMOTICZ_USERNAME
    domoticz_password = to_base64(str(app.config.DOMOTICZ_PASSWORD))
    with app.app_context():
        valid_pin = to_base64(get_pin())
    json_payload = {
        'pin': valid_pin,
        'client': 'Android Google Pixel 3',
        'client_uuid': str(uuid.uuid1()),
        'login': domoticz_login,
        'password': domoticz_password
    }
    response = post_json(client, 'api/beacon_auth/login', json_payload)
    response_json = json_response(response)
    assert response.status_code == 200
    assert 'access_token' in response_json
    access_token = response_json['access_token']
