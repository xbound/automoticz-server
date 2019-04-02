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
        self.project_id = app.config.PROJECT_ID

    @property
    def api(self):
        '''
        If is initialized returns Google API client instance.

        :return: bool
        '''
        if not hasattr(self, 'app'):
            return None
        return self.app.extensions.get('proximity')

    def init_api(self, credentials):
        ''' Initialize Proximity Beacon API

        :param credentials: google.oauth2.credentials.Credentials object  
        '''
        if credentials:
            proximitybeaconapi = discovery.build(
                OAUTH2.API_NAME, OAUTH2.API_VERSION, credentials=credentials)
            self.app.extensions['proximity'] = proximitybeaconapi