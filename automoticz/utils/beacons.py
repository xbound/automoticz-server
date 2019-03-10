import base64

from flask import _app_ctx_stack

from automoticz.utils.constants import OAUTH2
from googleapiclient import discovery


class ProximityBeaconAPI:
    '''
    Simple Flask extension for accessing Google Proxmity Beacon API.
    https://developers.google.com/resources/api-libraries/documentation/proximitybeacon/v1beta1/python/latest/
    '''

    def __init__(self, app=None, credentials=None):
        if app:
            self.init_app(app)
        if credentials:
            self.init_api(credentials)

    def init_app(self, app):
        '''
        Initialize Flask app for extension
        '''
        self.app = app
        self._project_id = app.config.PROJECT_ID

    @property
    def api(self):
        '''
        If is initialized returns Google API client instance.

        :return: bool
        '''
        if not hasattr(self, 'app'):
            return None
        return self.app.extensions.get('api')

    def init_api(self, credentials):
        ''' Initialize Proximity Beacon API

        :param credentials: google.oauth2.credentials.Credentials object  
        '''
        proximitybeaconapi = discovery.build(
            OAUTH2.API_NAME, OAUTH2.API_VERSION, credentials=credentials)
        self.app.extensions['api'] = proximitybeaconapi

    def get_default_auth_beacon_name(self):
        ''' Returns name of the beacon which property "auth" is set to 
        "true".

        :return: beacon name
        '''
        if hasattr(self, '_default_beacon_name'):
            return self._default_beacon_name
        api = self.app.extensions.get('api')
        query = 'status:active'
        response = api.beacons().list(q=query).execute()
        # Caching variable
        self._default_beacon_name = response['beacons'][0]['beaconName']
        return self._default_beacon_name

    def get_default_project_namespace(self):
        ''' Returns name of default namespace for attachments

        :return: default namespace name
        '''
        if hasattr(self, '_default_project_namespace'):
            return self._default_project_namespace
        api = self.app.extensions.get('api')
        query = {'projectId': self._project_id}
        resp = api.namespaces().list(**query).execute()
        # Caching variable
        self._default_project_namespace = resp['namespaces'][0][
            'namespaceName']
        return self._default_project_namespace

    def get_pin(self):
        ''' Checks if for beacon with given name u_token attachment
        is set.

        :param beacon_name: name of the beacon
        :param namespace: namespace
        '''
        beacon_name = self.get_default_auth_beacon_name()
        api = self.app.extensions.get('api')
        namespace = self.get_default_project_namespace().split('/')[1]
        namespaced_type = '{}/pin'.format(namespace)
        query = {'beaconName': beacon_name, 'namespacedType': namespaced_type}
        resp = api.beacons().attachments().list(**query).execute()
        b64_data = resp['attachments'][0]['data']
        return self._base64_to_str(b64_data)

    def is_pin_valid(self, pin):
        ''' Checks if recieved token is valid with current
        u_token attachment.

        :param pin: incomming u_token
        :return: True or False
        '''
        request_pin = self._base64_to_str(pin)
        current_pin = self.get_pin()
        return request_pin == current_pin

    def unset_pin(self):
        ''' Unsets "pin" type attachment on authentication beacon identified
        by beacon_name.
        '''
        beacon_name = self.get_default_auth_beacon_name()
        api = self.app.extensions.get('api')
        namespace = self.get_default_project_namespace().split('/')[1]
        namespaced_type = '{}/u_token'.format(namespace)
        query = {
            'beaconName': beacon_name,
            'namespacedType': namespaced_type,
        }
        resp = api.beacons().attachments().batchDelete(**query).execute()
        return resp

    def set_pin(self, pin):
        ''' Sets "u_token" type attachment on authentication beacon identified
        by beacon_name.

        :param pin: unique token
        '''
        beacon_name = self.get_default_auth_beacon_name()
        api = self.app.extensions.get('api')
        namespace = self.get_default_project_namespace().split('/')[1]
        namespaced_type = '{}/pin'.format(namespace)
        if self.get_pin() is not None:
            self.unset_pin()
        query = {
            'beaconName': beacon_name,
            'projectId': self._project_id,
            'body': {
                'namespacedType': namespaced_type,
                'data': self._str_to_base64(pin),
            }
        }
        resp = api.beacons().attachments().create(**query).execute()
        return resp

    def _base64_to_str(self, data):
        '''
        Encode string data to base64 string.
        '''
        return base64.b64decode(data.encode()).decode()

    def _str_to_base64(self, data):
        '''
        Decode base64 string to Python string.
        '''
        u_token_bytes = str.encode(data)
        return base64.b64encode(u_token_bytes).decode()
