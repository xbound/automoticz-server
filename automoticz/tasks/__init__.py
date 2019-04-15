from datetime import datetime
from dateutil import parser
import itertools

from flask import current_app as app

from automoticz.extensions import celery_app, db, cache
from automoticz.models import UsageLog
from automoticz.utils import get_users, get_used_devices, get_switch_history, get_temperature_history


def filter_log_duplicates(summary_log):
    tupled_logs = {tuple(log.items()) for log in summary_log}
    return [dict(tupled_log) for tupled_log in tupled_logs]


@cache.cached(key_prefix='fetch_devices_usage_map')
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


def fetch_logs_for_all_devices(from_date: datetime.date = None,
                               to_date: datetime.date = None,
                               filter_dup=True):
    # Create mapping between active devices
    # and users
    from_idx = int(app.config.FROM_IDX)
    to_idx = int(app.config.TO_IDX)
    devices_usage_map = fetch_devices_usage_map(from_idx, to_idx)

    def _is_between_dates(log):
        ''' Check if date from log in 
        selected time range.
        '''
        device_date = parser.parse(log['Date']).date()
        if from_date:
            if device_date < from_date:
                return False
        if to_date:
            if device_date > to_date:
                return False
        return True

    def _get_user_usage_log_for_device(device):
        ''' Method for fetching usage log
        based on device's type.
        '''
        device_type = device['device_type']
        device_idx = device['impostor_idx']
        if device_type == 'Switch':
            device_log = get_switch_history(device_idx)
        else:
            device_log = get_temperature_history(device_idx)
        return [
            dict(log, user_idx=device['user_idx']) for log in device_log
            if _is_between_dates(log)
        ]

    summary_log = list()
    for device_idx in devices_usage_map.keys():
        mapping = devices_usage_map[device_idx]
        # Get users' usage history for device identified by device_idx
        user_device_log = map(_get_user_usage_log_for_device, mapping)
        merged_log_records = itertools.chain.from_iterable(user_device_log)
        transformed = map(
            lambda v: {
                'idx': device_idx,
                'user_idx': v['user_idx'],
                'date': parser.parse(v['Date']),
                'status': v['Data']
            }, merged_log_records)
        summary_log.extend(transformed)
    # Removing duplicates
    if filter_dup:
        summary_log = filter_log_duplicates(summary_log)
    return summary_log
