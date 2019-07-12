import random

from flask import current_app as app
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_raw_jwt
from flask_restplus import Resource

from automoticz.tasks import set_beacon_pin
from automoticz.utils import beacon_auth, beacons, errors
from automoticz.utils.constants import RESPONSE_CODE, RESPONSE_MESSAGE
from automoticz.utils.beacon_auth import revoke_client_token

from . import namespace as api
from .helpers import register_reguest, register_response


@api.route('/login')
class Login(Resource):
    '''
    Device regestration endpoint.
    '''

    @api.expect(register_reguest, validate=True)
    @api.marshal_with(register_response)
    def post(self):
        data = api.payload
        pin = data.get('pin')
        login = data.get('login')
        password_b64 = data.get('password')
        if not beacons.is_pin_valid(pin):
            raise errors.InvalidPin()
        if not beacon_auth.is_valid_login(login, password_b64):
            raise errors.InvalidDomoticzLoginCredentilas()
        identity = beacon_auth.identity_exists(data)
        if not identity:
            identity = beacon_auth.add_new_identity(data)
        identity_client = beacon_auth.client_exists(data)
        if not identity_client:
            identity_client = beacon_auth.add_new_client(identity, data)
        access_token = create_access_token(identity_client.client_uuid)
        refresh_token = create_refresh_token(identity_client.client_uuid)
        beacon_auth.add_client_token(access_token, app.config.JWT_IDENTITY_CLAIM)
        beacon_auth.add_client_token(refresh_token, app.config.JWT_IDENTITY_CLAIM)
        set_beacon_pin.delay()
        return {
            'code': RESPONSE_CODE.LOGIN,
            'message': RESPONSE_MESSAGE.LOGIN,
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200


@api.route('/logout')
class Logout(Resource):

    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        revoke_client_token(jti)
        return {
            'code': RESPONSE_CODE.LOGOUT,
            'message': RESPONSE_MESSAGE.LOGOUT
        }, 200

