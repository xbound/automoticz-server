from automoticz.extensions import db
from automoticz.models import Device


def add_new_device_if_not_exists(data):
    '''
    Helper function for adding new device to database.

    :param data: device data
    :return: Device instance
    '''
    device = Device.query.filter_by(**data).first()
    if not device:
        device = Device(**data)
        db.session.add(device)
        db.session.commit()
    return device
