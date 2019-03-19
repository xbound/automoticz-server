import json
import re
import os
from datetime import datetime

import requests

from .constants import Values


class DomoticzAPI:
    '''
    Extension for making GET requests to Domoticz API
    '''

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
        self.verify_ssl = app.config.DOMOTICZ_VERIFY_SSL or False
        self.timeout = app.config.DOMOTICZ_API_TIMEOUT or 100
        self.auth = (api_username, api_password)
        self.app = app
        self.app.extensions['domoticz'] = self

    def api_call(self, request_params: dict) -> dict:
        '''
        Call Domoticz API with request parametres.
        '''
        response = requests.get(
            self.api_url,
            params=request_params,
            auth=self.auth,
            verify=self.verify_ssl,
            timeout=self.timeout)
        url = response.url
        json_response = response.json()
        status = json_response['status']
        if status != Values.OK_RESPONSE_STATUS:
            raise requests.exceptions.RequestException(
                'Status: {}. Request URI: {}'.format(status, url))
        return json_response
