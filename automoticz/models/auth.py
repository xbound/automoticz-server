from automoticz.extensions import db
from sqlalchemy.ext.declarative import declared_attr


class TokenMixin:

    @declared_attr
    def tokens(cls):
        return db.relationship('JWToken', backref='user', lazy='dynamic')


class User(TokenMixin, db.Model):
    ''' 
    Model for storing data about user.
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return str(dict(id=self.id, username=self.username))


class JWToken(db.Model):
    '''
    Model for storing JWT authorization tokens.
    '''
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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
                revoked=self.revoked
            ))
