from datetime import datetime

from flask_jwt_extended import decode_token
from sqlalchemy.orm.exc import NoResultFound

from automoticz.extensions import db
from automoticz.models import JWToken


def add_device_token(encoded_token, identity_claim):
    '''
    Adds a new token to the database. It is not revoked when it is added.

    :param identity_claim: configured key to get user identity
    '''
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_identity = decoded_token[identity_claim]
    expires = datetime.fromtimestamp(decoded_token['exp'])
    revoked = False

    token = JWToken(
        jti=jti,
        token_type=token_type,
        device_id=user_identity,
        expires=expires,
        revoked=revoked,
    )
    db.session.add(token)
    db.session.commit()


def revoke_device_token(token_jti, device_id):
    '''Revokes the given token

    Since we use it only on logout that already require a valid access token,
    if token is not found we raise an exception
    '''
    try:
        token = JWToken.query.filter_by(
            jti=token_jti, device_id=device_id).one()
        token.revoked = True
        db.session.commit()
    except NoResultFound:
        raise Exception('Could not find the token {}'.format(token_jti))


def is_token_revoked(decoded_token):
    '''
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    '''
    jti = decoded_token['jti']
    try:
        token = JWToken.query.filter_by(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True