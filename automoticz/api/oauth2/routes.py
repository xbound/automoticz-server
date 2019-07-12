from flask import current_app as app
from flask import redirect, request, session, url_for

from flask_restplus import Resource
from google_auth_oauthlib import flow

from automoticz.plugins.proximity import OAUTH2
from automoticz.utils.oauth2 import add_oauth2_credentials

from . import namespace


@namespace.route('/authorize')
class Authorize(Resource):

    def get(self):
        auth_flow = flow.Flow.from_client_secrets_file(
            app.config.CLIENT_SECRETS_FILE,
            scopes=OAUTH2.SCOPES,
        )
        auth_flow.redirect_uri = url_for('api.oauth2_callback', _external=True)
        authorization_url, state = auth_flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
        )
        session['state'] = state
        return redirect(authorization_url)


@namespace.route('/callback')
class Callback(Resource):

    def get(self):
        state = session['state']
        auth_flow = flow.Flow.from_client_secrets_file(
            app.config.CLIENT_SECRETS_FILE, scopes=OAUTH2.SCOPES, state=state)
        auth_flow.redirect_uri = url_for('api.oauth2_callback', _external=True)
    
        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_response = request.url
        auth_flow.fetch_token(authorization_response=authorization_response)
    
        credentials = auth_flow.credentials
        add_oauth2_credentials(credentials)
        return redirect(url_for('api.system_activate'))
