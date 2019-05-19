from automoticz.extensions import db

from .auth import JWToken


class Identity(db.Model):
    '''
    Model for storing data about present users.
    '''

    __tablename__ = 'identity'
    id = db.Column(db.Integer, primary_key=True)
    user_idx = db.Column(db.Integer, nullable=True)
    logged_in = db.Column(db.Boolean, default=False)
    clients = db.relationship('Client', backref='identity', lazy='dynamic')


class JWTBeacon(JWToken):
    '''
    Model for storing JWT authorization tokens.
    '''

    client_id = db.Column(db.String,
                          db.ForeignKey('clients.client_uuid'),
                          nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'client_id': self.client_id,
            'expires': self.expires,
            'revoked': self.revoked
        }


class Client(db.Model):
    '''
    Model for storing data about devices
    '''
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    client_uuid = db.Column(db.String, nullable=False)
    client = db.Column(db.String(50), nullable=True)
    tokens = db.relationship('JWTBeacon', backref='client', lazy='dynamic')
    identity_id = db.Column(db.Integer,
                            db.ForeignKey('identity.id'),
                            nullable=True)
