from automoticz.utils import constants


class AutomoticzError(Exception):
    message = 'Internal server error'
    code = constants.RESPONSE_CODE.DEFAULT_ERROR
    http_code = 500


class UnknownDomoticzLogin(AutomoticzError):
    message = constants.RESPONSE_MESSAGE.UNKNOWN_LOGIN
    code = 'UNKNOWN-LOGIN'
    http_code = 400


class InvalidDomoticzLoginCredentilas(AutomoticzError):
    message = constants.RESPONSE_MESSAGE.INVALID_CREDS
    code = 'INVALID-CREDS'
    http_code = 400


class InvalidPin(AutomoticzError):
    message = constants.RESPONSE_MESSAGE.INVALID_PIN
    code = 'INVALID-PIN'
    http_code = 400


class NotExistingDevice(AutomoticzError):
    message = constants.RESPONSE_MESSAGE.NOT_EXISTING_DEVICE
    code = 'NOT-EXISTING-DEVICE'
    http_code = 404


def make_error_response(error: Exception,
                        code=None,
                        message=None,
                        http_code=None):
    '''
    Make error response from exception. 

    :param error: exception
    '''
    if isinstance(error, AutomoticzError):
        return {
            'code': error.code,
            'message': error.message,
        }, error.http_code
    return {
        'code': code or constants.RESPONSE_CODE.DEFAULT_ERROR,
        'message': message or str(error),
    }, http_code or 500
