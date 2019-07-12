import json

from automoticz.utils.tool import str_to_base64

CONTENT_TYPE = 'application/json'


def get_json(client, url, headers=None):
    return client.get(url, headers=headers)


def post_json(client, url, json_dict=None, headers=None):
    return client.post(url,
                       data=json.dumps(json_dict),
                       content_type=CONTENT_TYPE,
                       headers=headers)


def delete_json(client, url, json_dict=None, headers=None):
    return client.delete(url,
                       data=json.dumps(json_dict),
                       content_type=CONTENT_TYPE,
                       headers=headers)


def json_response(response):
    return json.loads(response.data.decode('utf8'))


def to_base64(data):
    return str_to_base64(data)
