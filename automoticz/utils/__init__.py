import base64
from .constants import *

from .jwt import add_device_token
from .jwt import revoke_device_token
from .jwt import is_token_revoked

from .devices import *

from .oauth2 import *

from .home import *


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
