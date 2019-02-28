from flask import session
from flask_restplus import Namespace, Resource

from automoticz.utils.constants import MESSAGE
from automoticz.extensions import beaconapi
from automoticz.utils.db import get_default_credentials

activate_namespace = Namespace(
    'activate', description='Endpoint for initializing Proximity Beacon API.')


@activate_namespace.route('')
class Activate(Resource):
    '''
    Proximity Beacon API initialization endpoint.
    '''

    def get(self):
        if not beaconapi.is_initialized:
            creds = get_default_credentials()
            beaconapi.init_api(creds)
        return beaconapi.beacons().list().execute()