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


class OAUTH2:
    API_NAME = 'proximitybeacon'
    API_VERSION = 'v1beta1'
    SCOPES = ['https://www.googleapis.com/auth/userlocation.beacon.registry']
