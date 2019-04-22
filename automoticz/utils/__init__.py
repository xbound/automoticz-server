import base64
from .constants import *

from .auth import *
from .beacon_auth import *

from .oauth2 import *

from .home import *
from .analytics import *


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

from .beacons import *