import json

from tests.helpers import post_json, to_base64

def test_beacon_auth(mocker, app, client):
    mocker.patch('automoticz.utils.beacons.get_pin', return_value='0000')
    mocker.patch('automoticz.utils.beacons.get_default_auth_beacon_name',
                 return_value='beacons/test_beacon')
    mocker.patch('automoticz.utils.beacons.get_default_project_namespace',
                 return_value='project/automoticz-project')
    mocker.patch('automoticz.utils.beacons.unset_pin')
    mocker.patch('automoticz.utils.beacons.generate_pin', return_value='0000')
    mocker.patch('automoticz.api.endpoints.beacon_auth.routes.set_pin')

    json_payload = {'pin': to_base64('0000'), 'client': 'Android Google Pixel 3'}
    response = post_json(client, 'api/beacon_auth/login', json_payload)
    assert response.status_code == 200