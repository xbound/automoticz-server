from flask_jwt_extended import get_jti, decode_token

from automoticz.models import User, JWToken
from automoticz.commons.jwt import add_token_to_database
from automoticz.commons.jwt import is_token_revoked
from automoticz.commons.jwt import revoke_token


def test_add_token_to_database(app, access_token, refresh_token):
    with app.app_context():
        add_token_to_database(access_token, app.config.JWT_IDENTITY_CLAIM)
        add_token_to_database(refresh_token, app.config.JWT_IDENTITY_CLAIM)

        access_token_jti = get_jti(access_token)
        refresh_token_jti = get_jti(refresh_token)

        assert JWToken.query.filter_by(
            jti=access_token_jti).first() is not None
        assert JWToken.query.filter_by(
            jti=refresh_token_jti).first() is not None


def test_revoke_token(app, user, access_token, refresh_token):
    with app.app_context():
        add_token_to_database(access_token, app.config.JWT_IDENTITY_CLAIM)
        add_token_to_database(refresh_token, app.config.JWT_IDENTITY_CLAIM)

        access_token_jti = get_jti(access_token)
        refresh_token_jti = get_jti(refresh_token)

        revoke_token(access_token_jti, user.id)
        revoke_token(refresh_token_jti, user.id)

        is_token_revoked(decode_token(access_token))
        is_token_revoked(decode_token(refresh_token))