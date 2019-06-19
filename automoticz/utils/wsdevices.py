from flask import current_app as app
from automoticz.extensions import db, get_logger
from automoticz.models import WSDevice, WSCommand

logger = get_logger()

DEVICES = {}


def get_wsdevice_by_sid(sid: str):
    '''
    Get device by session id
    '''
    device_id = DEVICES.get(sid)
    if not device_id:
        return None
    return WSDevice.query.get(device_id)


def get_wsdevice_by_name(name: str) -> WSDevice:
    '''
    Get device by unique name
    '''
    return WSDevice.query.filter_by(name=name).first()


def get_ws_device(sid: str, device_info: dict):
    '''
    Get device by session id or name.
    '''
    device = get_wsdevice_by_sid(sid)
    if not device:
        name = device_info.get('name')
        if not name:
            return None
        return get_wsdevice_by_name(name)
    return device


def make_ws_command(data_dict: dict):
    return WSCommand(
        name=data_dict['name'],
        description=data_dict['description'],
        event=data_dict.get('event', 'message'),
        json_command=data_dict,
    )


def update_ws_command(command: WSCommand, data_dict: dict) -> bool:
    '''
    Update existing WS command intance.

    :param command: WSCommand instance to update
    :param data_dict: dict with values to update
    '''
    was_updated = False
    if command.description != data_dict['description']:
        command.description = data_dict['description']
        was_updated = True
    if command.event != data_dict.get('event', 'message'):
        command.event = data_dict.get('event', 'message')
        was_updated = True
    if command.json_command != data_dict:
        command.json_command = data_dict
        was_updated = True
    return was_updated


def register_ws_device(sid: str, device_info: dict) -> WSDevice:
    '''
    Add new device into register.
    '''
    device = get_wsdevice_by_sid(sid)
    if device:
        return False
    name = device_info['name']
    device = get_wsdevice_by_name(name)
    if device:
        DEVICES[sid] = device.id
        return False
    params = {
        'name':
        device_info['name'],
        'device_type':
        device_info['type'],
        'machine':
        device_info.get('machine'),
        'sysname':
        device_info.get('sysname'),
        'version':
        device_info.get('version'),
        'state':
        device_info.get('state') or device_info.get('value'),
        'commands':
        [make_ws_command(command) for command in device_info.get('commands')]
    }
    device = WSDevice(**params)
    db.session.add(device)
    db.session.commit()
    DEVICES[sid] = device.id
    return True


def get_ws_devices():
    wsdevices = WSDevice.query.all()
    return [{
        'id': ws['id'],
        'name': ws['name'],
        'machine': ws['machine'],
    } for ws in wsdevices]


def update_wsdevice_data(wsdevice: WSDevice, data: dict) -> bool:
    '''
    Update device data.
    '''
    was_modified = False
    for column in WSDevice.__table__.columns:
        if column.name in ('id', 'idx'):
            continue
        value = data[column.name]
        if column.name == 'commands':
            for command_data in value:
                command = wsdevice.commands.filter_by(
                    name=command_data['name'])
                if not command:
                    command = make_ws_command(command_data)
                    wsdevice.commands.append(command)
                    db.session.add(command)
                    was_modified = True
                else:
                    command_was_updated = update_ws_command(
                        command, command_data)
                    if command_was_updated: was_modified = True
        else:
            old_value = getattr(wsdevice, column.name, None)
            if value != old_value:
                setattr(wsdevice, column.name, value)
                was_modified = True
    wsdevice.state = data.get('state')
    if was_modified:
        db.session.commit()
    return was_modified


def get_device_command(device_id, command_id=None,
                       command_name=None) -> WSCommand:
    '''
    Get command instance of device.

    :param device_id: device id
    :param command_id:  command id
    :param command_id:  command name
    :return: WSCommand instance or None
    '''
    device = WSDevice.query.get(device_id)
    if not device:
        return None
    try:
        command = next(c for c in device.commands
                       if c.id == command_id or c.name == command_name)
    except StopIteration:
        command = None
    return command