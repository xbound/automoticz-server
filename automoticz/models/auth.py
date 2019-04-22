from automoticz.extensions import db

class JWToken(db.Model):
    '''
    Model for storing JWT authorization tokens.
    '''

    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    token_type = db.Column(db.String(10), nullable=True)
    expires = db.Column(db.DateTime, nullable=True)
    revoked = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'expires': self.expires,
            'revoked': self.revoked
        }
