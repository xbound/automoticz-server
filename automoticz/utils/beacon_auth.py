from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token

from automoticz.extensions import db
from automoticz.models import Client, JWTBeacon


def add_new_client_if_not_exists(data):
    '''
    Helper function for adding new device to database.

    :param data: device data
    :return: Device instance
    '''
    client = Client.query.filter_by(**data).first()
    if not client:
        client = Client(**data)
        db.session.add(client)
        db.session.commit()
    return client


def add_client_token(encoded_token, identity_claim):
    '''
    Adds a new token to the database. It is not revoked when it is added.

    :param identity_claim: configured key to get user identity
    '''
    decoded_token = decode_token(encoded_token)
    expiration = decoded_token.get('exp')
    params = {
        'jti': decoded_token['jti'],
        'token_type': decoded_token['type'],
        'client_id': decoded_token[identity_claim],
        'expires': datetime.fromtimestamp(expiration) if expiration else None,
        'revoked': False
    }
    token = JWTBeacon(**params)
    db.session.add(token)
    db.session.commit()


def revoke_client_token(token_jti, client_id):
    '''Revokes the given token

    Since we use it only on logout that already require a valid access token,
    if token is not found we raise an exception
    '''
    try:
        token = JWTBeacon.query.filter_by(
            jti=token_jti, client_id=client_id).one()
        token.revoked = True
        db.session.commit()
    except NoResultFound:
        raise Exception('Could not find the token {}'.format(token_jti))