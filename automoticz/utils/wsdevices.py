from flask import current_app as app

from automoticz.extensions import db, get_logger
from automoticz.models import WSCommand, WSDevice, WSState
from automoticz.utils import errors, tool

logger = get_logger()


class TwoWayDict(dict):
    '''
    Dictionary data structure for storing
    registered devices.
    '''

    def pop(self, key, default=None):
        if key in self:
            value = self[key]
            del self[key]
            return value
        else:
            return default

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

    def __len__(self):
        return dict.__len__(self) // 2


DEVICES = TwoWayDict()


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
        state.event = new_value
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
    )


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
        'device_type':
        device_info['type'],
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


def unregister_device(sid):
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


def is_device_online(device: WSDevice):
    '''
    Check if given WSDevice is online.

    :param device: WSDevice instance
    :return: bool value indicating if
    device was updated.
    '''
    return device.id in DEVICES


def get_ws_device_details(device_name):
    device = get_wsdevice_by_name(device_name)
    if not device:
        raise errors.NotExistingDevice()
    device_dict = device.to_dict()
    device_dict.update({
        'is_online': is_device_online(device),
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
        'is_online': is_device_online(device),
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
    type_new = data.get('type')
    machine_new = data.get('machine')
    sysname_new = data.get('sysname')
    version_new = data.get('version')
    if wsdevice.name != name_new and name_new:
        wsdevice.name = name_new
        was_modified = True
    if wsdevice.description != description_new and description_new:
        wsdevice.description = description_new
        was_modified = True
    if wsdevice.device_type != type_new and type_new:
        wsdevice.device_type = type_new
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
    was_modified = _update_wsstates(wsdevice, data.get('states', []))
    was_modified = _update_wscommands(wsdevice, data.get('commands', []))
    if was_modified:
        db.session.commit()
    return was_modified


def _update_wscommands(wsdevice: WSDevice, commands):
    was_modified = False
    for command_data in commands:
        command = wsdevice.commands.filter_by(name=command_data['name'])
        if not command:
            command = make_ws_command(command_data)
            wsdevice.commands.append(command)
            db.session.add(command)
            was_modified = True
        else:
            was_modified = update_ws_command(command, command_data)
    return was_modified


def _update_wsstates(wsdevice: WSDevice, states):
    was_modified = False
    for state_data in states:
        state = wsdevice.states.filter_by(name=state_data['name'])
        if not state:
            state = make_ws_state(state_data)
            wsdevice.states.append(state)
            db.session.add(state)
            was_modified = True
        else:
            was_modified = update_ws_state(state, state_data)
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
