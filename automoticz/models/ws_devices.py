import websocket
from automoticz.extensions import db

class WSDevice(db.Model):

    __tablename__ = 'wsdevices'

    id = db.Column(db.Integer, primary_key=True)
    idx = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    machine = db.Column(db.String(100), nullable=True)
    sysname = db.Column(db.String(100), nullable=True)
    version = db.Column(db.String(100), nullable=True)
    device_type = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(100), nullable=True)


    def __repr__(self):
        return str({
            'name': self.name,
            'machine': self.machine,
            'sysname': self.sysname,
            'version': self.version,
            'device_type': self.device_type,
            'status': self.status
        })


