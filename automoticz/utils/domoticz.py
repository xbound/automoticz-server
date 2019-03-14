import json
import re
import os
from datetime import datetime

import requests

class DomoticzAPI:
    '''
    Making GET requests to Domoticz API
    '''
    LOG_LEVEL_NORMAL = 1
    LOG_LEVEL_STATUS = 2
    LOG_LEVEL_ERROR = 4
    LOG_LEVEL_ALL = 268435455

    DEVICE_ALL = 'all'
    DEVICE_LIGHTS_SWITCHES = 'light'
    DEVICE_WEATHER = 'weather'
    DEVICE_TEMPERATURE = 'temp'
    DEVICE_UTILITY = 'utility'

    __datetime_regex = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}'

    def __init__(self,
                 domoticz_ip: str,
                 domoticz_port: int,
                 username: str,
                 password: str,
                 protocol='https'):
        self.api_url = '{protocol}://{domoticz_ip}:{domoticz_port}/json.htm'.format(
            protocol=protocol,
            domoticz_ip=domoticz_ip,
            domoticz_port=domoticz_port)
        self.username = username
        self.password = password

    def _get_log_datetime(self, log_message: str) -> datetime:
        '''
        Extract log datetime from log record
        '''
        datetime_str = re.search(self.__datetime_regex, log_message).group(0)
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')

    def _get_log_message(self, log_message: str) -> str:
        '''
        Extract message from log record
        '''
        return re.sub(self.__datetime_regex, '', log_message).strip()

    def get_logs(self, loglevel=LOG_LEVEL_NORMAL) -> dict:
        '''
        Returns dictionary of log records
        '''
        parametres = {
            'type': 'command',
            'param': 'getlog',
            'loglevel': loglevel
        }
        response = requests.get(
            self.api_url,
            params=parametres,
            auth=(self.username, self.password),
            verify=False,
            timeout=(30, 30))
        json_response = json.loads(response.text)

        log_records = list()
        for log in json_response['result']:
            log_record = {
                'level': log['level'],
                'message': self._get_log_message(log['message']),
                'datetime': self._get_log_datetime(log['message'])
            }
            log_records.append(log_record)
        return log_records

    def get_device_list(self, device_type=DEVICE_ALL):
        '''
        Returns dictionary of device records
        '''
        parametres = {
            'type': 'devices',
            'filter': device_type,
            'used': 'true',
            'order': 'Name'
        }
        response = requests.get(
            self.api_url,
            params=parametres,
            auth=(self.username, self.password),
            verify=False,
            timeout=(30, 30))
        json_response = json.loads(response.text)
        if json_response['status'] != 'OK':
            raise Exception('Domoticz response: {}'.format(
                json_response['status']))
        return json_response['result']

    def get_device(self, idx: int):
        '''
        Fetch device's info by idx
        '''
        parametres = {'type': 'devices', 'rid': idx}
        response = requests.get(
            self.api_url,
            params=parametres,
            auth=(self.username, self.password),
            verify=False,
            timeout=(30, 30))
        json_response = json.loads(response.text)
        if json_response['status'] != 'OK':
            raise Exception('Domoticz response: {}'.format(
                json_response['status']))
        return json_response['result'][0]
