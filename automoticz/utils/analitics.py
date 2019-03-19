import pandas as pd

from automoticz.domoticz.functions import get_switch_history, get_temperature_history
from automoticz.domoticz.constants import Values


def get_conditions_history(idx, time_range=Values.LOGS_RANGE_DAY):
    '''
    Get DateFrame with history from given device.
    '''
    records = get_temperature_history(idx, time_range)['result']
    raw_df = pd.DataFrame(records)
    raw_df['d'] = pd.to_datetime(raw_df['d'])
    df = raw_df.loc[:, ['d', 'hu', 'te']]
    df['date'] = df['d'].apply(lambda x: x.date())
    df['time'] = df['d'].apply(lambda x: x.time())
    df['weekday'] = df['d'].apply(lambda x: x.weekday())
    df['workday'] = df['weekday'].apply(lambda x: 0 <= x <= 4)
    df['humidity'] = df['hu'].astype('float')
    df['temperature'] = df['te'].astype('float')
    df.drop(['hu', 'te'], axis=1, inplace=True)
    return df.set_index('d')
