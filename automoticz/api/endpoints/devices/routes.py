import random
from flask_restplus import Resource
from flask import current_app as app
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token

from automoticz.extensions import jwt, db, beaconapi
from automoticz.models import Device

from automoticz.utils.constants import MESSAGE
from automoticz.utils.db import add_new_device_if_not_exists
from automoticz.utils.db import add_device_token
from automoticz.utils.db import revoke_device_token
from automoticz.utils.db import get_default_credentials

from . import devices_namespace as api
from .helpers import register_reguest
from .helpers import register_response
from .helpers import token_refresh_request
from .helpers import token_refresh_response
from .helpers import revoke_access_request
from .helpers import revoke_access_response
from .helpers import revoke_refresh_request
from .helpers import revoke_refresh_response


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
        # if not beaconapi.is_initialized:
            # creds = get_default_credentials()
            # beaconapi.init_api(creds)
        if not beaconapi.is_utoken_valid(u_token):
            return {'message': MESSAGE.INVALID_UTOKEN}
        device = add_new_device_if_not_exists(data)
        access_token = create_access_token(device.id)
        add_device_token(access_token, app.config.JWT_IDENTITY_CLAIM)
        new_utoken = str(random.randint(1, 999999999))
        beaconapi.set_utoken(new_utoken)
        return {
            'message': MESSAGE.LOGIN,
            'access_token': access_token,
        }
