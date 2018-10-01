import os
from flask import (
    render_template,
    session,
    redirect,
    json
)
from authlib.flask.client import OAuth
from core import app

# Setup OAuth configuration dict to pass to the template
auth0Config = {
    'clientId':os.getenv('AUTH0_CLIENT_ID'),
    'domain':os.getenv('AUTH0_DOMAIN'),
    'audience':os.getenv('AUTH0_API_AUDIENCE'),
    'spaRedirectUri':os.getenv('AUTH0_SPA_CALLBACK'),
    'redirectUri':os.getenv('AUTH0_CALLBACK'),
}

@app.route('/auth0')
def auth0_home_page():
    """
    Handle callback for the single page application authentication with OAuth.
    """
    return render_template('auth0/home.html', auth0Config=auth0Config)


#########################################################################
# Demo #1: Integrate with Auth0 by SPA (Single Page applcation.)
# 
# Demonstrates how to get user access token from a Single Page Application
# https://auth0.com/docs/quickstart/spa
#########################################################################

@app.route('/spa-callback')
def spa_callback_handling():
    """
    Handle callback for the single page application authentication with OAuth.
    """
    return render_template('auth0/callback.html', auth0Config=auth0Config)


#########################################################################
# Demo #2: Integrate with Auth0 by tranditional server rendered web app.
# 
# Demonstrates how to add user login to a Python web Application
# built with the Flask framework
# https://auth0.com/docs/quickstart/webapp/python
#########################################################################

# Setup OAuth
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=os.getenv('AUTH0_CLIENT_ID'),
    client_secret=os.getenv('AUTH0_CLIENT_SECRET'),
    api_base_url=os.getenv('AUTH0_API_BASE_URL'),
    access_token_url=os.getenv('AUTH0_ACCESS_TOKEN_URL'),
    authorize_url=os.getenv('AUTH0_AUTHORIZE_URL'),
    client_kwargs={
        'scope': 'openid profile',
    },
)


@app.route('/login')
def login():
    return auth0.authorize_redirect(
        redirect_uri= os.getenv('AUTH0_CALLBACK'),
        audience=os.getenv('AUTH0_API_BASE_URL') + '/userinfo')

# Here we're using the /callback route.
# This callback routing has to the same as the call back url 
# in the Auth0.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    return render_template('auth0/dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))
