import json

from flask import current_app as app
from google.oauth2.credentials import Credentials

from automoticz.extensions import db
from automoticz.models import OAuth2Credentials
from automoticz.models import OAuth2Scope


def add_oauth2_credentials(credentials: Credentials) -> OAuth2Credentials:
    ''' Add OAuth2 credentials to database if they do not
    exist in it.

    :param credentials: google.oauth2.credentials.Credentials object
    :return: OAuth2Credential object 
    '''
    oauth2_credentials = OAuth2Credentials.query.filter_by(
        client_id=credentials.client_id).first()
    model_updated = False
    if not oauth2_credentials:
        oauth2_credentials = OAuth2Credentials.from_creds(credentials)
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


def get_default_credentials() -> Credentials:
    ''' Returns default OAuth2 credentials from database used
    to fetch data from Google API.

    :return: google.oauth2.credentials.Credentials object
    '''
    if app.config.CREDENTIALS_FILE:
        creds =  oauth2_credentials_from_file(app.config.CREDENTIALS_FILE)
        if creds:
            return creds
    oauth2_credentials = OAuth2Credentials.query.filter(
        OAuth2Credentials.refresh_token.isnot(None)).first()
    if not oauth2_credentials:
        return None
    return oauth2_credentials.get_creds()


def oauth2_credentials_to_dict(credentials: Credentials) -> dict:
    '''
    Transforms Google OAuth2 Credentials to dictionary:

    :param credentials: Credentials object
    :return: dict
    '''
    return {
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'scopes': credentials.scopes
    }


def oauth2_credentials_to_file(credentials: Credentials, path: str = None):
    '''
    Serialize OAuth2Credentials to file identified by path.

    :param credentials: Credentials object.
    :param path: path to file.
    '''
    with open(path, 'w') as creds_file:
        json.dump(oauth2_credentials_to_dict(credentials), creds_file)


def oauth2_credentials_from_file(path: str = None) -> Credentials:
    '''
    Read OAuth2Credentials from file.

    :param path: path to file.
    '''
    try:
        with open(path, 'r') as creds_file:
            creds = json.load(creds_file)
        return Credentials(**creds)
    except:
        return None
