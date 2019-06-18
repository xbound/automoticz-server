import json

from automoticz.extensions import db


class JSONType(db.PickleType):
    '''
    JSON DB type is used to store JSON objects in the database
    '''

    impl = db.BLOB

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value, ensure_ascii=True)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class WSCommand(db.Model):

    __tablename__ = 'wscommands'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    event = db.Column(db.String(30), nullable=False)
    json_command = db.Column(JSONType, nullable=True)
    device_id = db.Column(db.Integer,
                            db.ForeignKey('wsdevices.id'),
                            nullable=True)


class WSDevice(db.Model):

    __tablename__ = 'wsdevices'

    id = db.Column(db.Integer, primary_key=True)
    idx = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    device_type = db.Column(db.String(100), nullable=False)
    machine = db.Column(db.String(100), nullable=True)
    sysname = db.Column(db.String(100), nullable=True)
    version = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    commands = db.relationship('WSCommand', backref='wsdevice', lazy='dynamic')


    def to_dict(self):
        return {
            'name': self.name,
            'machine': self.machine,
            'sysname': self.sysname,
            'version': self.version,
            'device_type': self.device_type,
            'state': self.state
        }

    def __repr__(self):
        return str(self.to_dict())
