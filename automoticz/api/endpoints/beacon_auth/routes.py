import random

from flask import current_app as app
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restplus import Resource

from automoticz.utils import MESSAGE
from automoticz.utils import add_client_token, add_new_client_if_not_exists
from automoticz.utils import is_pin_valid, set_pin, generate_pin

from automoticz.tasks import set_beacon_pin

from . import beacon_auth_namespace as api
from .helpers import register_reguest, register_response


@api.route('/login')
class Register(Resource):
    '''
    Device regestration endpoint.
    '''

    @api.expect(register_reguest, validate=True)
    @api.marshal_with(register_response)
    def post(self):
        data = api.payload
        pin = data.pop('pin')
        if not is_pin_valid(pin):
            return {'message': MESSAGE.INVALID_UTOKEN}, 400
        identity = add_new_client_if_not_exists(data)
        access_token = create_access_token(identity.id)
        refresh_token = create_refresh_token(identity.id)
        add_client_token(access_token, app.config.JWT_IDENTITY_CLAIM)
        add_client_token(refresh_token, app.config.JWT_IDENTITY_CLAIM)
        set_beacon_pin.delay()
        return {
            'message': MESSAGE.LOGIN,
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200
