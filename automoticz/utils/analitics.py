import pandas as pd

from automoticz.domoticz.functions import get_switch_history, get_temperature_history
from automoticz.domoticz.constants import Values


def get_conditions_history(idx, time_range=Values.LOGS_RANGE_DAY) -> pd.DataFrame:
    '''Get DateFrame with history from given device.

    :param idx: idx of device.
    :param time_range: time range from domoticz.constants.Values enum.
    :return: DataFrame object
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


def prepare_conditions_history(df: pd.DataFrame) -> pd.DataFrame:
    '''Formats values in columns for existing DataFrame.

    :param df: dataframe.
    :return: DataFrame object.
    '''
    df['d'] = pd.to_datetime(df['d'])
    df['date'] = df['d'].apply(lambda x: x.date())
    df['time'] = df['d'].apply(lambda x: x.time())
    df['weekday'] = df['d'].apply(lambda x: x.weekday())
    df['workday'] = df['weekday'].apply(lambda x: 0 <= x <= 4)
    df['humidity'] = df['humidity'].astype('float')
    df['temperature'] = df['temperature'].astype('float')
    return df.set_index('d')


def make_room_conditions_data(room_df: pd.DataFrame, out_df: pd.DataFrame):
    '''
    Creates training DataFrame

    :param room_df: dataframe with room's condition history.
    :param out_df: dataframe with ouside condition history. 
    '''