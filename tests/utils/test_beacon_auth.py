from tests.helpers import to_base64
from automoticz.utils.beacon_auth import *


def test_is_valid_login(app):
    domoticz_login = app.config.DOMOTICZ_USERNAME
    domoticz_password = to_base64(str(app.config.DOMOTICZ_PASSWORD))
    domoticz_password_invalid = to_base64('1234')
    with app.app_context():
        assert is_valid_login(domoticz_login, domoticz_password)
        assert not is_valid_login(domoticz_login, domoticz_password_invalid)
