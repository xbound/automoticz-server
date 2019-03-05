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
    def is_initialized(self):
        '''
        Checks if Proximity Beacon API is initialized.

        :return: bool
        '''
        ctx = _app_ctx_stack.top
        return hasattr(ctx, 'proximitybeaconapi')


    def init_api(self, credentials):
        ''' Initialize Proximity Beacon API

        :param credentials: google.oauth2.credentials.Credentials object  
        '''
        proximitybeaconapi = discovery.build(
            OAUTH2.API_NAME, OAUTH2.API_VERSION, credentials=credentials)
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'beacons'):
                ctx.proximitybeaconapi = proximitybeaconapi

    def get_default_auth_beacon_name(self):
        ''' Returns name of the beacon which property "auth" is set to 
        "true".

        :return: beacon name
        '''
        if hasattr(self,'_default_beacon_name'):
            return self._default_beacon_name
        ctx = _app_ctx_stack.top
        query = 'property:"auth=true"'
        response = ctx.proximitybeaconapi.beacons().list(q=query).execute()
        # Caching variable
        self._default_beacon_name = response['beacons'][0]['beaconName']
        return self._default_beacon_name

    def get_default_project_namespace(self):
        ''' Returns name of default namespace for attachments

        :return: default namespace name
        '''
        if hasattr(self, '_default_project_namespace'):
            return self._default_project_namespace
        ctx = _app_ctx_stack.top
        query = {'projectId': self._project_id}
        resp = ctx.proximitybeaconapi.namespaces().list(**query).execute()
        # Caching variable
        self._default_project_namespace = resp['namespaces'][0]['namespaceName']
        return self._default_project_namespace

    def get_utoken(self):
        ''' Checks if for beacon with given name u_token attachment
        is set.

        :param beacon_name: name of the beacon
        :param namespace: namespace
        '''
        beacon_name = self.get_default_auth_beacon_name()
        ctx = _app_ctx_stack.top
        namespace = self.get_default_project_namespace().split('/')[1]
        namespaced_type = '{}/u_token'.format(namespace)
        query = {
            'beaconName': beacon_name,
            'namespacedType': namespaced_type
        }
        resp = ctx.proximitybeaconapi.beacons().attachments().list(**query).execute()
        b64_data = resp['attachments'][0]['data']
        return self._base64_to_str(b64_data)

    def is_utoken_valid(self, u_token):
        ''' Checks if recieved token is valid with current
        u_token attachment.

        :param u_token: incomming u_token
        :return: True or False
        '''
        incomming_token = self._base64_to_str(u_token)
        current_token = self.get_utoken()
        return incomming_token == current_token


    def unset_utoken(self):
        ''' Unsets "u_token" type attachment on authentication beacon identified
        by beacon_name.

        :param beacon_name: name of the beacon
        '''
        beacon_name = self.get_default_auth_beacon_name()
        ctx = _app_ctx_stack.top
        namespace = self.get_default_project_namespace().split('/')[1]
        namespaced_type = '{}/u_token'.format(namespace)
        query = {
            'beaconName': beacon_name,
            'namespacedType': namespaced_type,
        }
        resp = ctx.proximitybeaconapi.beacons().attachments().batchDelete(
            **query).execute()
        return resp


    def set_utoken(self, u_token):
        ''' Sets "u_token" type attachment on authentication beacon identified
        by beacon_name.

        :param beacon_name: name of the beacon
        :param u_token: unique token
        '''
        beacon_name = self.get_default_auth_beacon_name()
        ctx = _app_ctx_stack.top
        namespace = self.get_default_project_namespace().split('/')[1]
        namespaced_type = '{}/u_token'.format(namespace)
        if self.get_utoken() is not None:
            self.unset_utoken()
        query = {
            'beaconName': beacon_name,
            'projectId': self._project_id,
            'body': {
                'namespacedType': namespaced_type,
                'data': self._str_to_base64(u_token),
            }
        }
        resp = ctx.proximitybeaconapi.beacons().attachments().create(
            **query).execute()
        return resp

    def _base64_to_str(self, data):
        return base64.b64decode(data.encode()).decode()

    def _str_to_base64(self, data):
        u_token_bytes = str.encode(data)
        return base64.b64encode(u_token_bytes).decode()
