import time

from flask_restplus import Resource
from flask_restplus import fields
from flask_jwt_extended import jwt_required

from automoticz.models import OAuth2Credentials
from automoticz.utils.constants import MESSAGE
from automoticz.extensions import beaconapi
from automoticz.utils.db import get_default_credentials

from . import maintanance_namespace

systime_response = maintanance_namespace.model(
    'System time  response', {
        'time':
        fields.String(
            description='Server time',
            example='Monday March, 04 2019 20:55:33'),
    })


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


@maintanance_namespace.route('/systime')
class SysTime(Resource):
    '''
    System time endpoint
    '''

    @jwt_required
    @maintanance_namespace.marshal_with(systime_response)
    def get(self):
        return {'time': time.strftime('%A %B, %d %Y %H:%M:%S')}
