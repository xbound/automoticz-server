from flask import _app_ctx_stack

from automoticz.utils.constants import OAUTH2
from googleapiclient import discovery


class BeaconAPI:
    '''
    Simple Flask extension for accessing Google Proxmity Beacon API.
    '''

    def __init__(self, app=None, credentials=None):
        self.init_app(app)
        self.init_api(credentials)
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        '''
        Initialize Flask app for extension
        '''
        self.app = app

    @property
    def is_initialized(self):
        '''
        Checks if Proximity Beacon API is initialized.

        :return: bool
        '''
        ctx = _app_ctx_stack.top
        return hasattr(ctx, 'beacons')

    def init_api(self, credentials):
        ''' Initialize Proximity Beacon API

        :param credentials: google.oauth2.credentials.Credentials object  
        '''
        proximitybeaconapi = discovery.build(
            OAUTH2.API_NAME, OAUTH2.API_VERSION, credentials=credentials)
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'beacons'):
                ctx.beacons = proximitybeaconapi.beacons()

    def __getattr__(self, name):
        ctx = _app_ctx_stack.top
        return getattr(ctx.beacons, name)
