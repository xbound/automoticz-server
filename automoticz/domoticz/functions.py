from flask import current_app as app

from .constants import Values


def get_settings():
    '''
    Returns Domoticz settings. 
    '''
    api = app.extensions['domoticz']
    return api.api_call({'type': 'settings'})


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
    return api.api_call(params)


def get_all_rooms():
    '''
    Returns list of all rooms.
    '''
    api = app.extensions['domoticz']
    params = {'type': 'plans', 'order': 'name', 'used': 'true'}
    return api.api_call(params)


def get_all_devices_in_room(idx):
    '''
    Returns all devices for room specified by
    idx.

    :param idx: room's idx number in Domoticz
    '''
    api = app.extensions['domoticz']
    params = {'type': 'command', 'param': 'getplandevices', 'idx': idx}
    return api.api_call(params)


def get_switch_history(idx, time_range=Values.LOGS_RANGE_DAY):
    '''
    Returns history of switch type device.

    :param idx: device's idx number in Domoticz
    '''
    api = app.extensions['domoticz']
    params = {'type': 'lightlog', 'idx': idx, 'range': time_range}
    return api.api_call(params)


def get_temperature_history(idx, time_range=Values.LOGS_RANGE_DAY):
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
    return api.api_call(params)


def get_users_data():
    '''
    Returns user's data.

    :return: users' data.
    '''
    # hardcoded
    return [
        {
            'idx': 1001,
            'name': 'User 1'
        },
        {
            'idx': 1002,
            'name': 'User 2'
        },
        {
            'idx': 1003,
            'name': 'User 3'
        },
        {
            'idx': 1004,
            'name': 'User 4'
        }
    ]