from flask import current_app as app

from automoticz.extensions import db, get_logger
from automoticz.models import WSCommand, WSDevice, WSState
from automoticz.utils import errors, tool

logger = get_logger()

DEVICES = tool.SidRegestry()


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


def get_ws_device(sid: str, device_info: dict, as_json=False):
    '''
    Get device by session id or name.
    '''
    device = get_wsdevice_by_sid(sid)
    if not device:
        name = device_info.get('name')
        if not name:
            return None
        device = get_wsdevice_by_name(name)
    if as_json:
        return get_ws_device_json(device)
    return device


def get_ws_device_json(device: WSDevice):
    data = device.to_dict()
    data.update({'is_online': is_device_online(device.id)})
    return data


def make_ws_command(data_dict: dict) -> WSCommand:
    '''
    Create WSCommand instance from given data
    dictionary.

    :param data_dict: dictionary with command
    data.
    :return: WSCommand instance
    '''
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


def update_ws_state(state: WSState, data_dict: dict) -> bool:
    was_updated = False
    new_desciption = data_dict.get('description')
    new_value = data_dict.get('value')
    if state.description != new_desciption and new_desciption:
        state.description = new_desciption
        was_updated = True
    if state.value != new_value and new_value:
        state.value = new_value
        was_updated = True
    return was_updated


def make_ws_state(data_dict: dict):
    '''
    Creates instance of WSState.
    '''
    return WSState(
        name=data_dict['name'],
        description=data_dict.get('description'),
        value=data_dict.get('value'),
        state_type=data_dict.get('state_type', 'text')
    )

def register_ws_device_domoticz(device: WSDevice):
    states = device.states.query.all()
    for state in states:
        if state.idx:
            continue

def register_ws_device(sid: str, device_info: dict) -> bool:
    '''
    Add new device into register.

    :param sid: session id.
    :param device_info: dictionary with 
    websocket device info.
    '''
    device = get_wsdevice_by_sid(sid)
    if device:
        update_wsdevice_data(device, device_info)
        return False
    name = device_info['name']
    device = get_wsdevice_by_name(name)
    if device:
        DEVICES[sid] = device.id
        update_wsdevice_data(device, device_info)
        return False
    params = {
        'name':
        device_info['name'],
        'description':
        device_info.get('description', ''),
        'machine':
        device_info.get('machine'),
        'sysname':
        device_info.get('sysname'),
        'version':
        device_info.get('version'),
        'states':
        [make_ws_state(state) for state in device_info.get('states')],
        'commands':
        [make_ws_command(command) for command in device_info.get('commands')]
    }
    params['description'] = tool.trim_str(params['description'], 500)
    device = WSDevice(**params)
    db.session.add(device)
    db.session.commit()
    DEVICES[sid] = device.id
    return True


def unregister_device(sid) -> WSDevice:
    '''
    Unregister device with given session id.

    :param sid: session id
    :return None or WSDevice instance.
    '''
    device = get_wsdevice_by_sid(sid)
    if not device:
        return False
    DEVICES.pop(sid)
    return device


def remove_unregister_wsdevice(device_name):
    '''
    Unregister device with given name and remove
    it from database.

    :param sid: session id
    :return None or WSDevice instance.
    '''
    wsdevice = get_wsdevice_by_name(device_name)
    sid = DEVICES[wsdevice.id]
    unregister_device(sid)
    db.session.delete()
    db.session.commit()


def is_device_online(device_id: int):
    '''
    Check if given WSDevice is online.

    :param device: WSDevice instance
    :return: bool value indicating if
    device was updated.
    '''
    if not isinstance(device_id, int):
        device_id = int(device_id)
    return device_id in DEVICES


def get_ws_device_details(device_id):
    if not isinstance(device_id, int):
        device_id = int(device_id)
    device = WSDevice.query.get(device_id)
    if not device:
        raise errors.NotExistingDevice()
    device_dict = device.to_dict()
    device_dict.update({
        'is_online': is_device_online(device.id),
    })
    return device_dict


def get_ws_devices():
    '''
    Returns list of dictionaries with websocket devices'
    short data.

    :return: list of dictionaries. 
    '''
    wsdevices = WSDevice.query.all()
    return [{
        'id': device.id,
        'name': device.name,
        'description': device.description,
        'is_online': is_device_online(device.id),
    } for device in wsdevices]


def update_wsdevice_data(wsdevice: WSDevice, data: dict) -> bool:
    '''
    Update device data.

    :param wsdevice: WSDevice instance.
    :param data: dictionary with new values.
    :return: bool value indicating if device data was modified.
    '''
    was_modified = False
    name_new = data.get('name')
    description_new = data.get('description')
    machine_new = data.get('machine')
    sysname_new = data.get('sysname')
    version_new = data.get('version')
    if wsdevice.name != name_new and name_new:
        wsdevice.name = name_new
        was_modified = True
    if wsdevice.description != description_new and description_new:
        wsdevice.description = description_new
        was_modified = True
    if wsdevice.machine != machine_new and machine_new:
        wsdevice.machine = machine_new
        was_modified = True
    if wsdevice.sysname != sysname_new and sysname_new:
        wsdevice.sysname = sysname_new
        was_modified = True
    if wsdevice.version != version_new and version_new:
        wsdevice.version = version_new
        was_modified = True
    wsstates_modified = _update_wsstates(wsdevice, data.get('states', []))
    wscommands_modified = _update_wscommands(wsdevice,
                                             data.get('commands', []))
    if wsstates_modified or wscommands_modified:
        was_modified = True
    if was_modified:
        db.session.commit()
    return was_modified


def _update_wscommands(wsdevice: WSDevice, commands):
    was_modified = False
    for command_data in commands:
        command = wsdevice.commands.filter_by(
            name=command_data['name']).first()
        if not command:
            command = make_ws_command(command_data)
            wsdevice.commands.append(command)
            db.session.add(command)
            was_modified = True
        else:
            modified = update_ws_command(command, command_data)
            if modified: was_modified = True
    return was_modified


def _update_wsstates(wsdevice: WSDevice, states):
    was_modified = False
    for state_data in states:
        state = wsdevice.states.filter_by(name=state_data['name']).first()
        if not state:
            state = make_ws_state(state_data)
            wsdevice.states.append(state)
            db.session.add(state)
            was_modified = True
        else:
            modified = update_ws_state(state, state_data)
            if modified: was_modified = True
    return was_modified


def get_device_command(device_id, command_id=None) -> WSCommand:
    '''
    Get command instance of device.

    :param device_name: device name
    :param command_id:  command id
    :param command_id:  command name
    :return: WSCommand instance or None
    '''
    device = WSDevice.query.get(device_id)
    if not device:
        return None
    command = device.commands.filter_by(id=command_id).first()
    return command
