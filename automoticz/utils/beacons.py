import base64

from flask import _app_ctx_stack

from automoticz.utils.constants import OAUTH2
from googleapiclient import discovery


class ProximityBeaconAPI:
    '''
    Simple Flask extension for accessing Google Proxmity Beacon API.
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
        self.project_id = app.config.PROJECT_ID

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
        ctx = _app_ctx_stack.top
        query = 'property:"auth=true"'
        response = ctx.proximitybeaconapi.beacons().list(q=query).execute()
        return response['beacons'][0]['beaconName']

    def get_default_beacon_namespace(self):
        ''' Returns name of default namespace for attachments

        :return: default namespace name
        '''
        ctx = _app_ctx_stack.top
        query = {'projectId': self.project_id}
        resp = ctx.proximitybeaconapi.namespaces().list(**query).execute()
        return resp['namespaces'][0]['namespaceName']

    def is_utoken_set(self, beacon_name, namespace=None):
        ''' Checks if for beacon with given name u_token attachment
        is set.

        :param beacon_name: name of the beacon
        :param namespace: namespace
        '''
        if namespace:
            namespaced_type = '{}/u_token'.format(namespace)
        # TODO Check if attachment "u_token" exists


    def set_utoken_attachment_for_beacon(self, beacon_name, u_token):
        ''' Sets "u_token" type attachment on authentication beacon identified
        by beacon_name.

        :param beacon_name: name of the beacon
        :param u_token: unique token
        '''
        ctx = _app_ctx_stack.top
        namespaceName = self.get_default_beacon_namespace().split('/')[1]
        u_token_bytes = str.encode(u_token)
        # TODO delete if set attachment "u_token" to avoid duplicates
        body = {
            'namespacedType': '{}/u_token'.format(namespaceName),
            'data': base64.b64encode(u_token_bytes).decode(),
        }
        resp = ctx.proximitybeaconapi.beacons().attachments().create(
            beaconName=beacon_name,
            projectId=self.project_id, 
            body=body).execute()
        return resp

    def __getattr__(self, name):
        ctx = _app_ctx_stack.top
        return getattr(ctx.proximitybeaconapi, name)
