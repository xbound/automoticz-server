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
        client_id=credentials.client_id).first()
    model_updated = False
    if not oauth2_credentials:
        oauth2_credentials = OAuth2Credential.from_creds(credentials)
        db.session.add(oauth2_credentials)
        model_updated = True
    else:
        for scope in credentials.scopes:
            oauth2_scope = OAuth2Scope.from_scope(scope)
            if oauth2_scope not in oauth2_credentials.scopes:
                oauth2_credentials.scopes.append(oauth2_scope)
                model_updated = True
        if oauth2_credentials.refresh_token is None:
            oauth2_credentials.refresh_token = credentials.refresh_token
            model_updated = True
    if model_updated:
        db.session.commit()
    return oauth2_credentials


def get_default_credentials():
    ''' Returns default OAtuh2 credentials from database used
    to fetch data from Google API.

    :return: google.oauth2.credentials.Credentials object
    '''
    oauth2_credentials = OAuth2Credential.query.filter(
        OAuth2Credential.refresh_token.isnot(None)).first()
    if not oauth2_credentials:
        return None
    return oauth2_credentials.get_creds()