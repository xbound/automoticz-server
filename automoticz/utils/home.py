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