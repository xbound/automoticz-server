import random

from flask import current_app as app
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restplus import Resource

from automoticz.utils import RESPONSE_MESSAGE
from automoticz.utils import errors
from automoticz.utils import rest
from automoticz.utils import *

from automoticz.tasks import set_beacon_pin

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
        if not is_pin_valid(pin):
            raise errors.InvalidPin()
        if not is_valid_login(login, password_b64):
            raise errors.InvalidDomoticzLoginCredentilas()
        identity = identity_exists(data)
        if not identity:
            identity = add_new_identity(data)
        identity_client = client_exists(data)
        if not identity_client:
            identity_client = add_new_client(identity, data)
        access_token = create_access_token(identity_client.client_uuid)
        refresh_token = create_refresh_token(identity_client.client_uuid)
        add_client_token(access_token, app.config.JWT_IDENTITY_CLAIM)
        add_client_token(refresh_token, app.config.JWT_IDENTITY_CLAIM)
        set_beacon_pin.delay()
        return {
            'code': RESPONSE_CODE.LOGIN,
            'message': RESPONSE_MESSAGE.LOGIN,
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200
