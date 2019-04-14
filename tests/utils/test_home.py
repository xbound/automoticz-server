from automoticz.utils.home import *


def test_get_settings(app):
    with app.app_context():
        assert get_settings()


def test_get_user_variables(app):
    with app.app_context():
        idx = 2
        assert get_user_variables(idx)


def test_get_device(app):
    with app.app_context():
        idx = 188
        assert get_device(idx)


def test_get_all_rooms(app):
    with app.app_context():
        assert get_all_rooms()


def test_get_all_devices_in_room(app):
    with app.app_context():
        idx = 7
        assert get_all_devices_in_room(idx)


def test_get_switch_history(app):
    with app.app_context():
        idx = 188
        assert get_switch_history(idx)


def test_get_temperature_history(app):
    with app.app_context():
        idx = 11
        assert get_temperature_history(idx)


def test_get_users(app):
    with app.app_context():
        assert get_users()


def test_get_used_devices(app):
    with app.app_context():
        assert get_used_devices()


def test_turn_switch_light(app):
    with app.app_context():
        idx = 188
        assert turn_switch_light(idx, 'On')
        assert turn_switch_light(idx, 'Off')


def test_fetch_devices_usage_map(app):
    with app.app_context():
        assert fetch_devices_usage_map(111, 187)
