from flask_restplus import Namespace, Resource

ping_namespace = Namespace(
    'ping', description='Ping endpoint for checking service availability.')


@ping_namespace.route('')
class Ping(Resource):
    '''
    Ping endpoint.
    '''

    def get(self):
        return {'status': 'OK'}, 200
