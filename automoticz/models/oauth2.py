from google.oauth2.credentials import Credentials

from automoticz.extensions import db

scopes_m2m = db.Table(
    'scopes',
    db.Column(
        'scope_id',
        db.Integer,
        db.ForeignKey('oauth2_scopes.id'),
        primary_key=True),
    db.Column(
        'credential_id',
        db.Integer,
        db.ForeignKey('oauth2_credentials.id'),
        primary_key=True),
)


class OAuth2Scope(db.Model):
    '''
    Google OAuth2 scope for resource
    '''
    __tablename__ = 'oauth2_scopes'

    id = db.Column(db.Integer, primary_key=True)
    scope = db.Column(db.String(100), unique=True, nullable=False)

    @classmethod
    def from_scope(cls, scope):
        ''' Create OAuth2Scope model object if not exists

        :param scope: str - scope name
        :return: OAuth2Scope object
        '''
        scopes = {row.scope: row for row in cls.query.all()}
        if not scope in scopes.keys():
            return cls(scope=scope)
        return scopes[scope]


class OAuth2Credentials(db.Model):
    '''
    Google OAuth2 credentials for accessing Proximity Beacon API
    '''
    __tablename__ = 'oauth2_credentials'

    id = db.Column(db.Integer, primary_key=True)
    token_uri = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.String(100), unique=True, nullable=False)
    client_secret = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String(250), nullable=False)
    refresh_token = db.Column(db.String(250), nullable=True)
    scopes = db.relationship(
        'OAuth2Scope',
        secondary=scopes_m2m,
        backref=db.backref('credentials', lazy=True),
        lazy='subquery')

    @classmethod
    def from_creds(cls, credentials):
        ''' Create model object from google.oauth2.credentials.Credentials

        :param credentials: google.oauth2.credentials.Credentials object
        :return: OAuth2Credential object
        '''
        scopes = credentials.scopes
        oauth2_scopes = [OAuth2Scope.from_scope(scope) for scope in scopes]
        oauth2_credential = OAuth2Credentials(
            client_id=credentials.client_id,
            token_uri=credentials.token_uri,
            client_secret=credentials.client_secret,
            token=credentials.token,
            refresh_token=credentials.refresh_token
        )
        for oauth2_scope in oauth2_scopes:
            oauth2_credential.scopes.append(oauth2_scope)
        return oauth2_credential

    def get_creds(self):
        ''' Get google.oauth2.credentials.Credentials object
        from model's object

        :return: google.oauth2.credentials.Credentials object
        '''
        return Credentials(**self.to_dict())

    def to_dict(self):
        return {
            'token_uri': self.token_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'token': self.token,
            'refresh_token': self.refresh_token,
            'scopes': [s.scope for s in self.scopes]
        }

    def __repr__(self):
        return str(self.to_dict())
