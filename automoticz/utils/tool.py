import base64
import json
from functools import wraps

from automoticz.extensions import cache
from automoticz.utils.constants import CACHE_LONG_TIMEOUT


def trim_str(value: str, chars_num: int, ending='...'):
    '''
    Trims string to given length.

    :param chars_num: numer of characters trim to.
    :return: str
    '''
    if len(value) > chars_num:
        return chars_num[:chars_num] + ending
    return value


def base64_to_str(data):
    '''
    Encode string data to base64 string.

    :param data: str to decode
    '''
    return base64.b64decode(data.encode()).decode()


def str_to_base64(data):
    '''
    Decode base64 string to Python string.

    :param data: str to encode
    '''
    encoded_string = str.encode(data)
    return base64.b64encode(encoded_string).decode()


def to_json(data: dict):
    '''
    Function to transform python dictionary to
    json string.

    :param data: dict to convert
    '''
    return json.dumps(data)


def to_dict(data: str):
    '''
    Function to transform python string to
    dictionary.

    :param data: str to convert
    '''
    return json.loads(data)


def cached_with_key(key):
    '''Caching decorator for saving function return
    value to cache.

    :param key: key.
    '''

    def wrap(func):
        def wrapper(*args, **kwargs):
            if kwargs.pop('cached', False):
                val = cache.get(key)
                if val:
                    return val
            val = func(*args, **kwargs)
            cache.set(key, val, timeout=CACHE_LONG_TIMEOUT)
            return val

        return wrapper

    return wrap
