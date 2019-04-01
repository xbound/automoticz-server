from datetime import datetime

from flask_jwt_extended import decode_token
from automoticz.models.auth import Device, JWToken


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


def add_new_device_if_not_exists(data):
    '''
    Helper function for adding new device to database.

    :param data: device data
    :return: Device instance
    '''
    device = Device.query.filter_by(**data).first()
    if not device:
        device = Device(**data)
        db.session.add(device)
        db.session.commit()
    return device