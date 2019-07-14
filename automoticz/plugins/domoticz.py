import json
import re
import os
from datetime import datetime

import requests

class CONSTANTS:
    LOGS_RANGE_DAY = 'day'
    LOGS_RANGE_MONTH = 'month'
    LOGS_RANGE_YEAR = 'year'
    OK_RESPONSE_STATUS = 'OK'
    ERROR_RESPONSE_STATUS = 'ERR'
    SWITCH_ON = 'On'
    SWITCH_OFF = 'Off'

class SENSORS:
    SWITCH = '0xF449'
    TEMP = '0x5101'
    TEXT = '0xF313'


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

    def api_call(self, request_params: dict, use_auth=True) -> dict:
        '''
        Call Domoticz API with request parametres.
        '''
        response = requests.get(
            self.api_url,
            params=request_params,
            auth=self.auth if use_auth else None,
            verify=self.verify_ssl,
            timeout=self.timeout)
        url = response.url
        json_response = response.json()
        status = json_response['status']
        if status != CONSTANTS.OK_RESPONSE_STATUS:
            raise requests.exceptions.RequestException(
                'Status: {}. Request URI: {}'.format(status, url))
        return json_response
