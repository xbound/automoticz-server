import re
from flask_restplus import fields

__BASE64_REGEX = re.compile(
    r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$')


class Base64String(fields.String):
    '''
    Base64 based string type field.
    '''

    __schema_type__ = 'string'
    __schema_format__ = 'base64'
    __schema_example__ = 'cHl0aG9u'

    def validate(self, value):
        if not value:
            return False if self.required else True
        return __BASE64_REGEX.match(value)


