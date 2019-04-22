import time

from flask_restplus import Resource
from flask_restplus import fields
from flask_jwt_extended import jwt_required

from automoticz.models import OAuth2Credentials
from automoticz.utils.constants import MESSAGE
from automoticz.extensions import proximity
from automoticz.utils import get_default_credentials
from automoticz.utils.beacons import get_default_auth_beacon_name

from . import system_namespace

systime_response = system_namespace.model(
    'System time  response', {
        'time':
        fields.String(
            description='Server time',
            example='Monday March, 04 2019 20:55:33'),
    })


@system_namespace.route('/ping')
class Ping(Resource):
    '''
    Ping endpoint.
    '''

    def get(self):
        return {'status': 'OK'}, 200


@system_namespace.route('/activate')
class Activate(Resource):
    '''
    Proximity Beacon API initialization endpoint.
    '''

    def get(self):
        if not proximity.api:
            creds = get_default_credentials()
            proximity.init_api(creds)
        beacon_name = get_default_auth_beacon_name()
        return {'beacon_name': beacon_name}, 200


@system_namespace.route('/systime')
class SysTime(Resource):
    '''
    System time endpoint
    '''

    @jwt_required
    @system_namespace.marshal_with(systime_response)
    def get(self):
        return {'time': time.strftime('%A %B, %d %Y %H:%M:%S')}, 200
