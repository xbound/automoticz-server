from automoticz.extensions import db

class BLEDevice(db.Model):
    '''
    Bluetooth LE device model.
    '''

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return str(dict(id=self.id, username=self.username))
