from flask import current_app as app
from flask import redirect, request, session, url_for
from google_auth_oauthlib import flow

from automoticz.utils.constants import OAUTH2
from automoticz.utils import add_oauth2_credentials

from .views import oauth2_blueprint


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
        app.config.CLIENT_SECRETS_FILE, scopes=OAUTH2.SCOPES, state=state)
    auth_flow.redirect_uri = url_for('oauth2.callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    auth_flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = auth_flow.credentials
    oauth2_credentials = add_oauth2_credentials(credentials)
    return redirect(url_for('api.maintanance_activate'))
