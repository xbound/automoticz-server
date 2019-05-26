import time

from flask_restplus import Resource
from flask_restplus import fields
from flask_jwt_extended import jwt_required

from automoticz.models import OAuth2Credentials
from automoticz.utils.constants import RESPONSE_MESSAGE
from automoticz.extensions import proximity
from automoticz.utils import get_default_credentials, get_users
from automoticz.utils.beacons import get_default_auth_beacon_name

from . import namespace

systime_response = namespace.model(
    'System time  response', {
        'time':
        fields.String(
            description='Server time',
            example='Monday March, 04 2019 20:55:33'),
    })


@namespace.route('/ping')
class Ping(Resource):
    '''
    Ping endpoint.
    '''

    def get(self):
        return {'status': 'OK'}, 200


@namespace.route('/activate')
class Activate(Resource):
    '''
    Proximity Beacon API initialization endpoint.
    '''

    def get(self):
        if not proximity.api:
            creds = get_default_credentials()
            proximity.init_api(creds)
        beacon_name = get_default_auth_beacon_name(cached=True)
        return {'beacon_name': beacon_name}, 200


@namespace.route('/systime')
class SysTime(Resource):
    '''
    System time endpoint
    '''

    @jwt_required
    @namespace.marshal_with(systime_response)
    def get(self):
        return {'time': time.strftime('%A %B, %d %Y %H:%M:%S')}, 200


@namespace.route('/users')
class Users(Resource):
    '''
    Users endpoint
    '''

    @jwt_required
    def get(self):
        users = get_users()
        for user_dict in users:
            user_dict.pop('Password')
            for key in user_dict.keys():
                user_dict[key.lower()] = user_dict.pop(key)
        return users
        
