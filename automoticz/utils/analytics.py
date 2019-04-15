from collections import defaultdict, Counter
import calendar
import datetime
import typing
import numpy
import pandas

from automoticz.domoticz import CONSTANTS

LOGLIST = typing.List[dict]

VALUE_MAPPING = {
    CONSTANTS.SWITCH_ON: 1, 
    CONSTANTS.SWITCH_OFF: 0,
    numpy.nan: -1,
    None: -1,
    1: 1,
    0: 0,
}


def make_users_weekday_schedule(log_records, pre_sort=True):
    '''
    Creates matrix of devices' usage schedule for each user. 

    Log records format:
    {
        'date': datetime.datetime(2019, 4, 1, 16, 39, 36),
        'idx': 64,
        'status': 'Off',
        'user_idx': 3
    }
    Response format:
    {
        user_idx-> 3: {
            Monday-> 0: {
                Device-> 26: {
                    Time -> datetime.time(0, 6): Status-> 1 (1 if On, 0 if Off),
                    datetime.time(0, 7): 0,
                    datetime.time(6, 22): 1,
                    datetime.time(18, 22): 0,
                    datetime.time(20, 26): 1,
                    datetime.time(20, 28): 0,
                    datetime.time(21, 38): 1,
                    datetime.time(21, 39): 0,
                    datetime.time(22, 55): 1,
                    datetime.time(23, 10): 0
                },
                27: {...},
            }
            Tuesday-> 1: {...},
            Wednesday-> 2: {...},
        },
    }

    :param log_records: devices' log history
    :param pre_sort: apply sorting by `date` for log_record
    '''
    if pre_sort:
        log_records = sorted(log_records, key=lambda l: l['date'])

    def formated_time(dt: datetime.datetime):
        time = dt.replace(second=0, microsecond=0).time()
        return time.strftime('%H:%M')

    user_weekday_data = {}
    for log in log_records:
        weekday = log['date'].weekday()
        time = formated_time(log['date'])
        device = log['idx']
        status = log['status']
        user = log['user_idx']

        if user not in user_weekday_data:
            user_weekday_data[user] = {}
        if weekday not in user_weekday_data[user]:
            user_weekday_data[user][weekday] = {}
        if device not in user_weekday_data[user][weekday]:
            user_weekday_data[user][weekday][device] = {}
        user_weekday_data[user][weekday][device].update(
            {time: VALUE_MAPPING[status]})

    return user_weekday_data


def schedule_to_pandas(users_weekdays_schedule):
    '''
    Takes result of make_users_weekday_schedule function
    and transforms values by key `weekday` to pandas.Dataframe
    object.

    :param users_weekday_schedule: result of make_users_weekday_schedule
    '''

    users_weekdays_schedule_pd = defaultdict(dict)
    for user in users_weekdays_schedule:
        for weekday in users_weekdays_schedule[user]:
            weekday_matrix_orig = users_weekdays_schedule[user][weekday]
            weekday_matrix_rows = [
                {'idx': device, **device_activations}
                for device, device_activations in weekday_matrix_orig.items()
            ]
            df = pandas.DataFrame(weekday_matrix_rows)
            df.set_index('idx', inplace=True)
            users_weekdays_schedule_pd[user][weekday] = df
    return users_weekdays_schedule_pd

