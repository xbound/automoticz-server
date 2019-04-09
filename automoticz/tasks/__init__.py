from datetime import datetime
from dateutil import parser
import itertools

from flask import current_app as app

from automoticz.extensions import celery_app, db, cache
from automoticz.models import UsageLog
from automoticz.utils import fetch_devices_usage_map, get_switch_history, get_temperature_history


def fetch_logs_for_all_devices(from_date: datetime.date = None,
                               to_date: datetime.date = None):
    # Create mapping between active devices
    # and users
    devices_usage_map = fetch_devices_usage_map(111, 187)

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

    # All log records will be appended to this list
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
    return summary_log
