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
