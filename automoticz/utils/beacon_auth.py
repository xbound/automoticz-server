from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token

from automoticz.extensions import db
from automoticz.models import Identity, Client, JWTBeacon
from automoticz.utils.tool import str_to_base64
from automoticz.utils.home import get_users, log_in


def is_valid_login(login, password_b64):
    '''
    Verify if login credentials are valid credentials
    of Domoticz user.

    :param login: Domoticz login
    :param password_b64: base64 encoded password
    '''
    login_b64 = str_to_base64(login)
    result = log_in(login_b64, password_b64)
    if 'Revision' not in result and 'SystemName' not in result:
        return False
    return True


def identity_exists(data):
    '''
    Verify if identity exists in database

    :param data: request data dict
    :return: None or Identity object
    '''
    login = data.get('login')
    user_map = {u['Username']: u['idx'] for u in get_users()}
    identity_idx = int(user_map[login])
    return Identity.query.filter_by(user_idx=identity_idx).first()


def client_exists(data):
    '''
    Verify if client exists in database

    :param data: request data dict
    :return: None or Client object
    '''
    client_uuid = data.get('client_uuid')
    return Client.query.filter_by(client_uuid=client_uuid).first()


def add_new_client(identity: Identity, data):
    '''
    Helper function for adding new device to database.

    :param data: device data
    :return: Device instance
    '''
    client_uuid = data.get('client_uuid')
    client = Client(client_uuid=client_uuid)
    client_name = data.pop('client', 'Unknown Client {}'.format(client.id))
    client.client = client_name
    db.session.add(client)
    identity.clients.append(client)
    db.session.commit()
    return client


def add_new_identity(data):
    '''
    Helper function for adding new identity to database.

    :param data: device data
    :return: Identity instance
    '''
    login = data.get('login')
    user_map = {u['Username']: u['idx'] for u in get_users()}
    user_idx = int(user_map[login])
    identity = Identity(user_idx=user_idx)
    db.session.add(identity)
    db.session.commit()
    return identity


def add_client_token(encoded_token, identity_claim, client):
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


def revoke_client_token(token_jti):
    '''Revokes the given token

    Since we use it only on logout that already require a valid access token,
    if token is not found we raise an exception
    '''
    try:
        token = JWTBeacon.query.filter_by(jti=token_jti).one()
        token.revoked = True
        db.session.commit()
    except NoResultFound:
        raise Exception('Could not find the token {}'.format(token_jti))