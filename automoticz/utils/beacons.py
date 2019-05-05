import random

from automoticz.extensions import proximity
from automoticz.utils import base64_to_str, str_to_base64, cached_with_key


@cached_with_key('beacon')
def get_default_auth_beacon_name():
    ''' Returns name of the beacon which property "auth" is set to 
    "true".

    :return: beacon name
    '''
    api = proximity.api
    query = 'status:active'
    response = api.beacons().list(q=query).execute()
    default_beacon_name = response['beacons'][0]['beaconName']
    return default_beacon_name


@cached_with_key('project_namespace')
def get_default_project_namespace():
    ''' Returns name of default namespace for attachments

    :return: default namespace name
    '''
    api = proximity.api
    query = {'projectId': proximity.project_id}
    resp = api.namespaces().list(**query).execute()
    default_project_namespace = resp['namespaces'][0]['namespaceName']
    return default_project_namespace.split('/')[1]


@cached_with_key('pin')
def get_pin():
    ''' Checks if for beacon with given name pin attachment
    is set.

    :param beacon_name: name of the beacon
    :param namespace: namespace
    '''
    api = proximity.api
    beacon_name = get_default_auth_beacon_name(cached=True)
    namespace = get_default_project_namespace(cached=True)
    namespaced_type = '{}/pin'.format(namespace)
    query = {'beaconName': beacon_name, 'namespacedType': namespaced_type}
    resp = api.beacons().attachments().list(**query).execute()
    b64_data = resp['attachments'][0]['data']
    return base64_to_str(b64_data)


def is_pin_valid(pin):
    ''' Checks if recieved token is valid with current
    u_token attachment.

    :param pin: incomming u_token
    :return: True or False
    '''
    request_pin = base64_to_str(pin)
    current_pin = get_pin(cached=True)
    return request_pin == current_pin


def unset_pin():
    ''' Unsets "pin" type attachment on authentication beacon identified
    by beacon_name.
    '''
    api = proximity.api
    beacon_name = get_default_auth_beacon_name(cached=True)
    namespace = get_default_project_namespace(cached=True)
    namespaced_type = '{}/pin'.format(namespace)
    query = {
        'beaconName': beacon_name,
        'namespacedType': namespaced_type,
    }
    resp = api.beacons().attachments().batchDelete(**query).execute()
    return resp


def set_pin(pin):
    ''' Sets "pin" type attachment on authentication beacon identified
    by beacon_name.

    :param pin: unique token
    '''
    api = proximity.api
    beacon_name = get_default_auth_beacon_name(cached=True)
    namespace = get_default_project_namespace(cached=True)
    namespaced_type = '{}/pin'.format(namespace)
    if get_pin() is not None:
        unset_pin()
    query = {
        'beaconName': beacon_name,
        'projectId': proximity.project_id,
        'body': {
            'namespacedType': namespaced_type,
            'data': str_to_base64(pin),
        }
    }
    resp = api.beacons().attachments().create(**query).execute()
    return resp


def generate_pin():
    ''' Generates new pin.

    :return: pin 
    '''
    new_pin = str(random.randint(1, 999999999))
    return new_pin