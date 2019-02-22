from automoticz.extensions import db
from automoticz.models import OAuth2Credential
from automoticz.models import OAuth2Scope


def add_oauth2_credentials(credentials):
    ''' Add OAuth2 credentials to database if they do not
    exist in it.

    :param credentials: google.oauth2.credentials.Credentials object
    :return: OAuth2Credential object 
    '''
    oauth2_credentials = OAuth2Credential.query.filter_by(
        client_id=credentials.client_id, ).first()
    if not oauth2_credentials:
        oauth2_credentials = OAuth2Credential.from_creds(credentials)
        db.session.add(oauth2_credentials)
        db.session.commit()
    return oauth2_credentials