from flask import session
from flask_restplus import Namespace, Resource

from automoticz.models import OAuth2Credential

ping_namespace = Namespace(
    'ping', description='Ping endpoint for checking service availability.')


@ping_namespace.route('')
class Ping(Resource):
    '''
    Ping endpoint.
    '''

    def get(self):
        _id = session.get('__ID__')
        if _id:
            return OAuth2Credential.query.filter_by(
                client_id=_id
            ).first().to_dict(), 200
        return {'status': 'OK'}, 200
