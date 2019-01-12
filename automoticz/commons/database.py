from automoticz.extensions import db
from automoticz.models import User, BLEDevice


def add_new_user_if_not_exists(data):
    '''
    Helper function for adding new user to database.

    :param data: user's data
    :return: user instance
    '''
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        user = User(username=data['username'])
        if data.get('blu_id'):
            user.devices.append(BLEDevice(name=data['blu_id']))
        db.session.add(user)
        db.session.commit()
    return user


def add_new_ble_device_if_not_exists(user, data):
    '''
    Helper function for adding new bluetooth device to database.

    :param user: linked user
    :param data: device's data
    :return: bluetooth device instance
    '''
    ble_device = BLEDevice.query.filter_by(name=data['blu_id']).first()
    if not ble_device:
        ble_device = BLEDevice(name=data['blu_id'])
        user.devices.append(ble_device)
        db.session.commit()
    return ble_device