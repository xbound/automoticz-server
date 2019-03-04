from automoticz.extensions import db
from sqlalchemy.ext.declarative import declared_attr


class User(db.Model):
    ''' 
    Model for storing data about user.
    '''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    tokens = db.relationship('JWToken', backref='user', lazy='dynamic')

    def __repr__(self):
        return str(dict(id=self.id, username=self.username))


class Device(db.Model):
    '''
    Model for storing data about devices
    '''
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(50), nullable=True)
    model = db.Column(db.String(50), nullable=True)
    brand = db.Column(db.String(50), nullable=True)
    manufacturer = db.Column(db.String(50), nullable=True)
    product = db.Column(db.String(100), nullable=True)
    tokens = db.relationship('JWToken', backref='device', lazy='dynamic')


class JWToken(db.Model):
    '''
    Model for storing JWT authorization tokens.
    '''

    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=True)
    expires = db.Column(db.DateTime, nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return str(
            dict(
                id=self.id,
                jti=self.jti,
                token_type=self.token_type,
                user_id=self.user_id,
                expires=self.expires,
                revoked=self.revoked))
