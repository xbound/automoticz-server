from flask import current_app as app
from flask import session
from flask import redirect
from flask import request
from flask import url_for
from google.oauth2 import credentials
from google_auth_oauthlib import flow
from googleapiclient import discovery

from automoticz.api.views import oauth2_blueprint
from automoticz.utils.db import add_oauth2_credentials
from automoticz.utils.db import get_default_credentials
from automoticz.utils.constants import OAUTH2


@oauth2_blueprint.route('/authorize')
def authorize():
    auth_flow = flow.Flow.from_client_secrets_file(
        app.config.CLIENT_SECRETS_FILE,
        scopes=OAUTH2.SCOPES,
    )
    auth_flow.redirect_uri = url_for('oauth2.callback', _external=True)
    authorization_url, state = auth_flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
    )
    session['state'] = state
    return redirect(authorization_url)


@oauth2_blueprint.route('/callback')
def callback():
    state = session['state']
    auth_flow = flow.Flow.from_client_secrets_file(
        app.config.CLIENT_SECRETS_FILE,
        scopes=OAUTH2.SCOPES,
        state=state
    )
    auth_flow.redirect_uri = url_for('oauth2.callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    auth_flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = auth_flow.credentials
    oauth2_credentials = add_oauth2_credentials(credentials)
    session['__ID__'] = oauth2_credentials.id
    return redirect(url_for('api.maintanance_activate'))

