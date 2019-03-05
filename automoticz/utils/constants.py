class ENV:
    DEVELOPMENT = 'development'
    TESTING = 'testing'
    PRODUCTION = 'production'


class MESSAGE:
    LOGIN = 'LOGIN'
    REGISTER = 'REGISTER'
    REFRESH = 'REFRESH'
    REVOKE_ACCESS = 'REVOKE-ACCESS'
    REVOKE_REFRESH = 'REVOKE-REFRESH'
    API_NOT_INITIALIZED = 'API-NOT-INITIALIZED'
    NO_CREDENTIALS_PROVIDED = 'NO-CREDENTIALS-PROVIDED'
    INVALID_UTOKEN = 'INVALID-UTOKEN'


class OAUTH2:
    API_NAME = 'proximitybeacon'
    API_VERSION = 'v1beta1'
    SCOPES = ['https://www.googleapis.com/auth/userlocation.beacon.registry']
