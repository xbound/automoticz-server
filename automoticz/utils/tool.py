import base64
import json
import pprint
from functools import wraps

from automoticz.extensions import cache, get_logger
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


def str_to_json(data):
    return json.loads(data)


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


class SidRegestry(dict):
    '''
    Dictionary data structure for storing
    registered devices.
    '''

    def __init__(self):
        self.sids = []

    def pop(self, key, default=None):
        if key in self:
            value = self[key]
            del self[key]
            return value
        else:
            return default

    def __setitem__(self, key, value):
        # assuming first key is sid
        self.sids.append(key)
        if key in self:
            del self[key]
            if key in self.sids:
                self.sids.remove(key)
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        v = self[key]
        dict.__delitem__(self, v)
        dict.__delitem__(self, key)
        if key in self.sids:
            self.sids.remove(key)
        if v in self.sids:
            self.sids.remove(v)

    def __len__(self):
        return dict.__len__(self) // 2


log = get_logger()

request_log_message = ''' Incoming request:
Headers: 
{headers}
Body: 
{body}
'''

response_log_message = ''' Outgoing response:
Headers: 
{headers}
Body: 
{body}
'''


def log_request(request):
    body = request.get_data()
    if isinstance(body, bytes):
        body = body.decode('utf-8')
    message = request_log_message.format(
        headers=request.headers,
        body=body,
    )
    log.debug(message)

def log_response(response):
    body = response.get_data()
    if isinstance(body, bytes):
        body = body.decode('utf-8')
    print(response.headers)
    message = response_log_message.format(
        headers=response.headers,
        body=body,
    )
    log.debug(message)


def pretty_log_info(message, data):
    log.info(message.format(pprint.pformat(data, indent=2)))