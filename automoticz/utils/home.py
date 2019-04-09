from flask import current_app as app

from automoticz.extensions import cache
from automoticz.utils import DOMOTICZ


@cache.cached(key_prefix='domoticz_settings')
def get_settings():
    '''
    Returns Domoticz settings. 
    '''
    api = app.extensions['domoticz']
    return api.api_call({'type': 'settings'})['result']


@cache.memoize()
def get_user_variables(idx=None):
    '''
    Returns all user variables or returns one
    specified by `idx` argument.

    :param idx: idx of variable 
    '''
    api = app.extensions['domoticz']
    params = {'type': 'command', 'param': 'getuservariables'}
    if idx:
        params['idx'] = idx
    return api.api_call(params)['result']


@cache.memoize()
def get_device(idx):
    '''
    Fetch device information identified by idx from Domoticz API.

    :param idx: idx of device.
    :return: dict with device information.
    '''
    api = app.extensions['domoticz']
    params = {'type': 'devices', 'rid': idx}
    return api.api_call(params)['result']


@cache.cached(key_prefix='domoticz_all_rooms')
def get_all_rooms():
    '''
    Returns list of all rooms.
    '''
    api = app.extensions['domoticz']
    params = {'type': 'plans', 'order': 'name', 'used': 'true'}
    return api.api_call(params)['result']


@cache.memoize()
def get_all_devices_in_room(idx):
    '''
    Returns all devices for room specified by
    idx.

    :param idx: room's idx number in Domoticz
    '''
    api = app.extensions['domoticz']
    params = {'type': 'command', 'param': 'getplandevices', 'idx': idx}
    return api.api_call(params)['result']


@cache.memoize()
def get_switch_history(idx, time_range=DOMOTICZ.LOGS_RANGE_DAY):
    '''
    Returns history of switch type device.

    :param idx: device's idx number in Domoticz
    '''
    api = app.extensions['domoticz']
    params = {'type': 'lightlog', 'idx': idx, 'range': time_range}
    return api.api_call(params)['result']


@cache.memoize()
def get_temperature_history(idx, time_range=DOMOTICZ.LOGS_RANGE_DAY):
    '''
    Gets temperature, humidity and pressure history from device
    with idx and given range.

    :param idx: device's idx number in Domoticz
    :param time_range: time range (day, month, year)
    '''
    api = app.extensions['domoticz']
    params = {
        'type': 'graph',
        'sensor': 'temp',
        'idx': idx,
        'range': time_range
    }
    return api.api_call(params)['result']


@cache.cached(key_prefix='domoticz_users')
def get_users():
    '''
    Returns user's data.

    :return: users' data.
    '''
    # hardcoded
    api = app.extensions['domoticz']
    params = {'type': 'users'}
    return api.api_call(params)['result']


@cache.cached(key_prefix='domoticz_used_devices')
def get_used_devices():
    '''Returns dictionary of device records.

    :return: list of devices.
    '''
    api = app.extensions['domoticz']
    params = {
        'displayhidden': '1',
        'filter': 'all',
        'type': 'devices',
        'used': 'all',
    }
    return api.api_call(params)['result']

@cache.memoize()
def fetch_devices_usage_map(from_idx: int, to_idx: int) -> dict:
    ''' 
    Fetch all devices registered on Domoticz server.
    '''
    users = get_users()
    username_idx_map = {user['Username']: int(user['idx']) for user in users}
    devices = get_used_devices()
    devicename_idx_map = {device['Name']: int(device['idx']) for device in devices}
    devices_usage_mapping = {}

    def _idx_in_between(idx):
        if idx < from_idx:
            return False
        if idx > to_idx:
            return False
        return True

    def _split_device_name(name):
        splitted = name.split('-')
        return tuple(s.strip() for s in splitted)

    def _append_to_mapping(device):
        device_name, user_label = _split_device_name(device['Name'])
        device_id = devicename_idx_map[device_name]
        if device_id not in devices_usage_mapping:
            devices_usage_mapping[device_id] = []
        user_id = app.config.USER_MAPPING[user_label]
        user_id = username_idx_map[user_id]
        impostor_idx = int(device['idx'])
        devices_usage_mapping[device_id].append({
            'impostor_idx': impostor_idx,
            'user_idx': user_id,
            'device_type': device['SubType'],
        })

    for device in devices:
        impostor_idx = int(device['idx'])
        if _idx_in_between(impostor_idx):
            _append_to_mapping(device)

    return devices_usage_mapping