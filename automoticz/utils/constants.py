class ENV:
    DEVELOPMENT = 'development'
    TESTING = 'testing'
    PRODUCTION = 'production'


class RESPONSE_MESSAGE:
    LOGIN = 'LOGIN'
    REGISTER = 'REGISTER'
    REFRESH = 'REFRESH'
    REVOKE_ACCESS = 'REVOKE-ACCESS'
    REVOKE_REFRESH = 'REVOKE-REFRESH'
    API_NOT_INITIALIZED = 'API-NOT-INITIALIZED'
    NO_CREDENTIALS_PROVIDED = 'NO-CREDENTIALS-PROVIDED'
    INVALID_PIN = 'Invalid pin was sent to server'
    INVALID_CREDS = 'Invalid login or password'
    UNKNOWN_LOGIN = 'Invalid user login'


class RESPONSE_CODE:
    DEFAULT_ERROR = 'ERR'
    INVALID_PIN = 'INVALID-PIN'
    INVALID_CREDS = 'INVALID-CREDS'


PIN_ATTACHMENT_KEY = 'pin'
CACHE_PIN_KEY = 'pin'
CACHE_SET_PIN_KEY = 'set_pin'
CACHE_SET_PIN_KEY_TIMEOUT = 30
CACHE_LONG_TIMEOUT = 100