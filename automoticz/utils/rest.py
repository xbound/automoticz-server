import re
from flask_restplus import fields, Model

__BASE64_REGEX = re.compile(
    r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$')


class Base64String(fields.String):
    '''
    Base64 based string type field.
    '''

    __schema_type__ = 'string'
    __schema_format__ = 'base64'
    __schema_example__ = '--base64-encoded-value--'

    def validate(self, value):
        if not value:
            return False if self.required else True
        return __BASE64_REGEX.match(value)


message_field = fields.String(description='Response message',
                              example='Login successful')

code_field = fields.String(description='Response code', example='LOGIN')

access_token_field = fields.String(
    description='Access token',
    example=
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwiZnJlc2giOmZhbHNlLCJleHAiOjE1NTY0NzM4MzYsIm5iZiI6MTU1NjQ3MjkzNiwiaWRlbnRpdHkiOjUsImp0aSI6ImE4OTI1Mzk1LWQyM2QtNGRmNC04MDZlLWNhMWRiMGVhNTgzOSIsImlhdCI6MTU1NjQ3MjkzNn0.HhWTa70hnAtyf6WzoT8hBj_4WTo2nYjVBvlJGHREqEk'
)
refresh_token_field = fields.String(
    description='Refresh token',
    example=
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6NSwidHlwZSI6InJlZnJlc2giLCJuYmYiOjE1NTY0NzI5MzYsImp0aSI6IjU4OTNhYTI2LWM2YTYtNGM1MC1iZmIzLWM5MjA4NGNhNTcxNCIsImlhdCI6MTU1NjQ3MjkzNn0.Rown-44Zg1kpAnXKubTWwGaDER4deqW2PdqQLTmTTs0'
)

wsdevice_id_field = fields.Integer(description='Device id')
wsdevice_name_field = fields.String(description='WebSocket device name')
wsdevice_description_field = fields.String(description='WebSocket device description')
wsdevice_machine_filed = fields.String(description='WebSocket device machine')
wsdevice_sysname_field = fields.String(description='WebSocket device version')
wsdevice_device_type_field = fields.String(description='WebSocket device type')
wsdevice_state_field =  fields.String(description='WebSocket device state')
wsdevice_is_online_field = fields.Boolean(description='Websocket device connection status')

response_base = {
    'message': message_field,
    'code': code_field,
}
