import typing

from flask import current_app as app

from automoticz.extensions import cache, domoticz
from automoticz.domoticz import CONSTANTS

IdxType = typing.Union[int, str]


@cache.cached(key_prefix='domoticz_settings')
def get_settings():
    '''
    Returns Domoticz settings. 
    '''

    return domoticz.api_call({'type': 'settings'})


@cache.memoize()
def get_user_variables(idx: IdxType=None):
    '''
    Returns all user variables or returns one
    specified by `idx` argument.

    :param idx: idx of variable 
    '''

    params = {'type': 'command', 'param': 'getuservariables'}
    if idx:
        params['idx'] = idx
    return domoticz.api_call(params)['result']


@cache.memoize()
def get_device(idx: IdxType):
    '''
    Fetch device information identified by idx from Domoticz API.

    :param idx: idx of device.
    :return: dict with device information.
    '''
    params = {'type': 'devices', 'rid': idx}
    return domoticz.api_call(params)['result']


@cache.cached(key_prefix='domoticz_all_rooms')
def get_all_rooms():
    '''
    Returns list of all rooms.
    '''
    params = {'type': 'plans', 'order': 'name', 'used': 'true'}
    return domoticz.api_call(params)['result']


@cache.memoize()
def get_all_devices_in_room(idx: IdxType):
    '''
    Returns all devices for room specified by
    idx.

    :param idx: room's idx number in Domoticz
    '''
    params = {'type': 'command', 'param': 'getplandevices', 'idx': idx}
    return domoticz.api_call(params)['result']


@cache.memoize()
def get_switch_history(idx: IdxType, time_range=CONSTANTS.LOGS_RANGE_DAY):
    '''
    Returns history of switch type device.

    :param idx: device's idx number in Domoticz
    '''
    params = {'type': 'lightlog', 'idx': idx, 'range': time_range}
    return domoticz.api_call(params)['result']


@cache.memoize()
def get_temperature_history(idx: IdxType, time_range=CONSTANTS.LOGS_RANGE_DAY):
    '''
    Gets temperature, humidity and pressure history from device
    with idx and given range.

    :param idx: device's idx number in Domoticz
    :param time_range: time range (day, month, year)
    '''
    params = {
        'type': 'graph',
        'sensor': 'temp',
        'idx': idx,
        'range': time_range
    }
    return domoticz.api_call(params)['result']


@cache.cached(key_prefix='domoticz_users')
def get_users():
    '''
    Returns user's data.

    :return: users' data.
    '''
    params = {'type': 'users'}
    return domoticz.api_call(params)['result']


@cache.cached(key_prefix='domoticz_used_devices')
def get_used_devices():
    '''Returns dictionary of device records.

    :return: list of devices.
    '''
    params = {
        'displayhidden': '1',
        'filter': 'all',
        'type': 'devices',
        'used': 'all',
    }
    return domoticz.api_call(params)['result']


def turn_switch_light(idx: IdxType, switchMode: str):
    '''
    Command for turning switch or light on/off

    :param idx: idx of device.
    :param switchMode: On or Off
    :return: dict with device information.
    '''
    params = {
        'type': 'command',
        'param': 'switchlight',
        'idx': idx,
        'switchcmd': switchMode
    }
    return domoticz.api_call(params)



@cache.memoize()
def fetch_devices_usage_map(from_idx: int, to_idx: int) -> dict:
    ''' 
    Fetch logging imposter devices from the server limited by given range
    and create map for each device according to each user.

    :param from_idx: idx of first device, range beggining.
    :param to_idx: idx of last device, range ending.
    :return: dict 
    '''
    users = get_users()
    username_idx_map = {user['Username']: int(user['idx']) for user in users}
    devices = get_used_devices()
    devicename_idx_map = {
        device['Name']: int(device['idx'])
        for device in devices
    }
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
            'impostor_idx':
            impostor_idx,
            'user_idx':
            user_id,
            'device_type':
            device['SubType'],
        })

    for device in devices:
        impostor_idx = int(device['idx'])
        if _idx_in_between(impostor_idx):
            _append_to_mapping(device)

    return devices_usage_mapping