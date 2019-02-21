from flask import current_app as app
from flask import session
from flask import redirect
from google.oauth2 import credentials
from google_auth_oauthlib import flow 
from googleapiclient import discovery

from automoticz.api.views import oauth2_blueprint

API_NAME = 'proximitybeacon'
API_VERSION = 'v1beta1'
SCOPES = ['https://www.googleapis.com/auth/userlocation.beacon.registry']

@oauth2_blueprint.route('/authorize')
def authorize():
    auth_flow = flow.Flow.from_client_secrets_file(
      app.config.CLIENT_SECRETS_FILE, scopes=SCOPES)
    authorization_url, state = auth_flow.authorization_url(
      access_type='offline',
      include_granted_scopes='true')
    
    auth_flow.redirect_uri = app.config.REDIRECT_URL
    session['state'] = state
    return redirect(authorization_url)

@oauth2_blueprint.route('/callback')
def oauth2callback():
    pass

