from flask_restplus import Resource
from . import maintanance_namespace
from automoticz.models import OAuth2Credentials
from automoticz.utils.constants import MESSAGE
from automoticz.extensions import beaconapi
from automoticz.utils.db import get_default_credentials


@maintanance_namespace.route('/ping')
class Ping(Resource):
    '''
    Ping endpoint.
    '''

    def get(self):
        return {'status': 'OK'}, 200


@maintanance_namespace.route('/activate')
class Activate(Resource):
    '''
    Proximity Beacon API initialization endpoint.
    '''

    def get(self):
        if not beaconapi.is_initialized:
            creds = get_default_credentials()
            beaconapi.init_api(creds)
        return beaconapi.beacons().list().execute()