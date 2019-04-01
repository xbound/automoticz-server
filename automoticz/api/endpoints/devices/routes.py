import random

from flask import current_app as app
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restplus import Resource

from automoticz.extensions import beaconapi, db, jwt
from automoticz.models import Device
from automoticz.utils import (add_device_token, add_new_device_if_not_exists,
                              get_default_credentials, revoke_device_token)
from automoticz.utils.constants import MESSAGE

from . import devices_namespace as api
from .helpers import (register_reguest, register_response,
                      revoke_access_request, revoke_access_response,
                      revoke_refresh_request, revoke_refresh_response,
                      token_refresh_request, token_refresh_response)


@api.route('/register')
class Register(Resource):
    '''
    Device regestration endpoint.
    '''

    @api.expect(register_reguest)
    @api.marshal_with(register_response)
    def post(self):
        data = api.payload
        u_token = data.pop('u_token')
        if not beaconapi.is_pin_valid(u_token):
            return {'message': MESSAGE.INVALID_UTOKEN}
        device = add_new_device_if_not_exists(data)
        access_token = create_access_token(device.id)
        add_device_token(access_token, app.config.JWT_IDENTITY_CLAIM)
        new_utoken = str(random.randint(1, 999999999))
        beaconapi.set_pin(new_utoken)
        return {
            'message': MESSAGE.LOGIN,
            'access_token': access_token,
        }
