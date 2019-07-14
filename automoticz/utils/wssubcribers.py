from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token

from automoticz.extensions import db, socketio
from automoticz.models import Identity, Client, JWTBeacon
from automoticz.utils.tool import str_to_base64, SidRegestry
from automoticz.utils.home import get_users, log_in

SUBSCRIBERS = SidRegestry()


def get_client_by_uuid(client_uuid) -> Client:
    return Client.query.filter_by(client_uuid=client_uuid).first()


def get_subscriber_by_sid(sid: str):
    '''
    Get device by session id
    '''
    client_uuid = SUBSCRIBERS.get(sid)
    if not client_uuid:
        return None
    return get_client_by_uuid(client_uuid)


def unregister_subsriber(sid):
    '''
    Unregister subsriber with given session id.

    :param sid: session id
    :return None or Client instance.
    '''
    subscriber = get_subscriber_by_sid(sid)
    if not subscriber:
        return None
    SUBSCRIBERS.pop(sid)
    return subscriber


def register_subscriber(sid: str, data: dict):
    client_uuid = data.get('client_uuid')
    if not client_uuid:
        return False
    client = get_client_by_uuid(client_uuid)
    if any(client.tokens.filter_by(revoked=False).all()):
        SUBSCRIBERS[sid] = client.client_uuid
        return True
    return False
