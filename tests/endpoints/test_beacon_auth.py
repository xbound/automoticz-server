import json
import uuid

from tests.helpers import post_json, to_base64, json_response


def test_login(mocker, app, client):
    mocker.patch('automoticz.utils.beacons.get_pin', return_value='0000')
    mocker.patch('automoticz.app.get_beacon_pin.delay')
    mocker.patch('automoticz.utils.beacons.get_default_auth_beacon_name',
                 return_value='beacons/test_beacon')
    mocker.patch('automoticz.utils.beacons.get_default_project_namespace',
                 return_value='project/automoticz-project')
    mocker.patch('automoticz.utils.beacons.unset_pin')
    mocker.patch('automoticz.utils.beacons.generate_pin', return_value='0000')
    mocker.patch('automoticz.api.beacon_auth.routes.set_beacon_pin')

    domoticz_login = app.config.DOMOTICZ_USERNAME
    domoticz_password = to_base64(str(app.config.DOMOTICZ_PASSWORD))
    domoticz_password_invalid = to_base64('1234')
    json_payload = {
        'pin': to_base64('0000'),
        'client': 'Android Google Pixel 3',
        'client_uuid': str(uuid.uuid1()),
        'login': domoticz_login,
        'password': domoticz_password
    }
    response = post_json(client, 'api/beacon_auth/login', json_payload)
    response_json = json_response(response)
    assert response.status_code == 200
    assert 'access_token' in response_json
    # assert 'refresh_token' in response_json

    json_payload = {
        'pin': to_base64('0000'),
        'client': 'Android Google Pixel 3',
        'client_uuid': str(uuid.uuid1()),
        'login': domoticz_login,
        'password': domoticz_password_invalid
    }
    response = post_json(client, 'api/beacon_auth/login', json_payload)
    response_json = json_response(response)
    assert response.status_code == 400
    assert 'INVALID-CREDS' == response_json['message']

    json_payload = {'client': 'Android Google Pixel 3'}
    response = post_json(client, 'api/beacon_auth/login', json_payload)
    assert response.status_code == 400

    json_payload = {
        'pin': to_base64('1111'),
        'client': 'Chrome Browser',
        'client_uuid': str(uuid.uuid1()),
        'login': domoticz_login,
        'password': domoticz_password
    }
    response = post_json(client, 'api/beacon_auth/login', json_payload)
    response_json = json_response(response)
    assert response.status_code == 400
    assert 'INVALID-PIN' == response_json['message']