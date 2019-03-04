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

    @property
    def latest_utoken(self):
        return self._data

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
        if self._default_beacon_name:
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
        if self._default_project_namespace:
            return self._default_project_namespace
        ctx = _app_ctx_stack.top
        query = {'projectId': self._project_id}
        resp = ctx.proximitybeaconapi.namespaces().list(**query).execute()
        # Caching variable
        self._default_project_namespace = resp['namespaces'][0]['namespaceName']
        return self._default_project_namespace

    def is_utoken_set(self, beacon_name):
        ''' Checks if for beacon with given name u_token attachment
        is set.

        :param beacon_name: name of the beacon
        :param namespace: namespace
        '''
        ctx = _app_ctx_stack.top
        namespace = self.get_default_project_namespace().split('/')[1]
        namespaced_type = '{}/u_token'.format(namespace)
        query = {
            'beaconName': beacon_name,
            'namespacedType': namespaced_type
        }
        resp = ctx.proximitybeaconapi.beacons().attachments().list(**query).execute()
        return any(a for a in resp['attachments'] if a['namespacedType'] == namespaced_type)

    def unset_utoken(self, beacon_name):
        ''' Unsets "u_token" type attachment on authentication beacon identified
        by beacon_name.

        :param beacon_name: name of the beacon
        '''
        ctx = _app_ctx_stack.top
        namespaced_type = self._namespaced_type
        if not namespaced_type:
            namespace = self.get_default_project_namespace().split('/')[1]
            namespaced_type = '{}/u_token'.format(namespace)
        query = {
            'beaconName': beacon_name,
            'namespacedType': namespaced_type,
        }
        resp = ctx.proximitybeaconapi.beacons().attachments().batchDelete(
            **query).execute()
        return resp


    def set_utoken(self, beacon_name, u_token):
        ''' Sets "u_token" type attachment on authentication beacon identified
        by beacon_name.

        :param beacon_name: name of the beacon
        :param u_token: unique token
        '''
        ctx = _app_ctx_stack.top
        u_token_bytes = str.encode(u_token)
        namespaced_type = self._namespaced_type
        if not namespaced_type:
            namespace = self.get_default_project_namespace().split('/')[1]
            namespaced_type = '{}/u_token'.format(namespace)
        if self.is_utoken_set(beacon_name):
            self.unset_utoken(beacon_name)
        query = {
            'beaconName': beacon_name,
            'projectId': self._project_id,
            'body': {
                'namespacedType': namespaced_type,
                'data': base64.b64encode(u_token_bytes).decode(),
            }
        }
        resp = ctx.proximitybeaconapi.beacons().attachments().create(
            **query).execute()
        self._data = base64.b64decode(resp['data'].encode()).decode()
        self._namespaced_type = resp.get('namespacedType')
        return resp

    def __getattr__(self, name):
        ctx = _app_ctx_stack.top
        if hasattr(ctx.proximitybeaconapi, name):
            return getattr(ctx.proximitybeaconapi, name)
        else:
            return None
