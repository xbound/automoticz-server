import json
import re
import os
from datetime import datetime

import requests


class DomoticzAPI:
    '''
    Extension for making GET requests to Domoticz API
    '''

    LOGS_RANGE_DAY = 'day'
    LOGS_RANGE_MONTH = 'month'
    LOGS_RANGE_YEAR = 'year'

    def __init__(self, app=None):
        '''
        Extension initialization
        '''
        if app:
            self.init_app(app)

    def init_app(self, app):
        '''
        App initialization
        '''
        api_protocol = 'https' if not app.config.DOMOTICZ_USE_HTTP else 'http'
        api_host = app.config.DOMOTICZ_HOST
        api_port = app.config.DOMOTICZ_PORT
        api_username = app.config.DOMOTICZ_USERNAME
        api_password = app.config.DOMOTICZ_PASSWORD
        self.api_url = '{protocol}://{host}:{port}/json.htm'.format(
            protocol=api_protocol,
            host=api_host,
            port=api_port,
        )
        self.auth = (api_username, api_password)
        self.app = app

    def api_call(self, request_params: dict) -> dict:
        '''
        Call Domoticz API with request parametres.
        '''
        verify_ssl = self.app.config.DOMOTICZ_VERIFY_SSL or False
        response = requests.get(
            self.api_url,
            params=request_params,
            auth=self.auth,
            verify=verify_ssl,
            timeout=(30, 30))
        return response.json()