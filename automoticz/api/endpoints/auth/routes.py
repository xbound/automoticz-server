from flask_restplus import Resource
from flask import current_app as app
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_refresh_token_required

from automoticz.api.endpoints.auth import auth_namespace as api
from .helpers import login_reguest
from .helpers import login_response
from .helpers import token_refresh_request
from .helpers import token_refresh_response
from .helpers import revoke_access_request
from .helpers import revoke_access_response
from .helpers import revoke_refresh_request
from .helpers import revoke_refresh_response

from automoticz.extensions import jwt, db
from automoticz.models import User

from automoticz.commons.constants import MESSAGE
from automoticz.commons.database import add_new_user_if_not_exists
from automoticz.commons.jwt import add_token_to_database
from automoticz.commons.jwt import is_token_revoked
from automoticz.commons.jwt import revoke_token


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return User.query.get(identity)


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


@api.route('/login')
class Login(Resource):
    '''
    Auth login/registration endpoint.
    '''

    @api.expect(login_reguest)
    @api.marshal_with(login_response)
    def post(self):
        data = api.payload
        user = add_new_user_if_not_exists(data)
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        add_token_to_database(access_token, app.config.JWT_IDENTITY_CLAIM)
        add_token_to_database(refresh_token, app.config.JWT_IDENTITY_CLAIM)
        return {
            'message': MESSAGE.LOGIN,
            'access_token': access_token,
            'refresh_token': refresh_token
        }


@api.route('/refresh')
class TokenRefresh(Resource):
    '''
    Token refresh endpoint.
    '''

    @api.expect(token_refresh_request)
    @api.marshal_with(token_refresh_response)
    @jwt_refresh_token_required
    def post(self):
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity)
        add_token_to_database(new_access_token, app.config.JWT_IDENTITY_CLAIM)
        return {'message': MESSAGE.REFRESH, 'access_token': new_access_token}


@api.route('/revoke_access')
class RevokeAccess(Resource):
    '''
    Logout endpoint.
    '''

    @api.expect(revoke_access_request)
    @api.marshal_with(revoke_access_response)
    @jwt_required
    def post(self):
        identity = get_jwt_identity()
        jti = get_raw_jwt()['jti']
        revoke_token(jti, identity)
        user = User.query.get(identity)
        return {'message': 'REVOKE-ACCESS', 'username': user.username}


@api.route('/revoke_refresh')
class RevokeRefresh(Resource):
    '''
    Logout endpoint.
    '''

    @api.expect(revoke_refresh_request)
    @api.marshal_with(revoke_refresh_response)
    @jwt_refresh_token_required
    def post(self):
        identity = get_jwt_identity()
        jti = get_raw_jwt()['jti']
        revoke_token(jti, identity)
        user = User.query.get(identity)
        return {'message': MESSAGE.REVOKE_REFRESH, 'username': user.username}
