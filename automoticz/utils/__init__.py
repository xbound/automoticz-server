import base64
from .constants import *

from .jwt import add_device_token
from .jwt import revoke_device_token
from .jwt import is_token_revoked

from .devices import *

from .oauth2 import add_oauth2_credentials, get_default_credentials

from .home import *

all = [
    'ENV',
    'MESSAGE',
    'OAUTH2',
    'DOMOTICZ',
    'add_token_to_database',
    'revoke_token',
    'is_token_revoked',
    'add_oauth2_credentials',
    'get_default_credentials',
    'add_token_to_database',
    'is_token_revoked',
    'add_oauth2_credentials',
    'get_default_credentials',
    'add_new_device_if_not_exists',
    'add_device_token',
    'revoke_device_token',
    'get_light_and_switches',
    'base64_to_str',
    'str_to_base64',
]

def base64_to_str(data):
    '''
    Encode string data to base64 string.
    '''
    return base64.b64decode(data.encode()).decode()

def str_to_base64(data):
    '''
    Decode base64 string to Python string.
    '''
    u_token_bytes = str.encode(data)
    return base64.b64encode(u_token_bytes).decode()