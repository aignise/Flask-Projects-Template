from flask import Blueprint, render_template, redirect, url_for, session
from flask_oauthlib.client import OAuth
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()


auth = Blueprint('auth', __name__)
oauth = OAuth()

google = oauth.remote_app(
    'google',
    consumer_key= os.environ.get("GOOGLE_CLIENT_ID"),
    consumer_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    request_token_params={
        'scope': 'email profile',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@auth.route('/login')
def login():
    return google.authorize(callback=url_for('auth.authorized', _external=True))

@auth.route('/logout')
def logout():
    session.pop('google_token', None)
    session.pop('user_email', None)
    return redirect(url_for('home'))


@auth.route('/login/callback')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')

    session['user_email'] = user_info.data['email']
    session['user_name'] = user_info.data['name']
    session['user_picture'] = user_info.data['picture']

    
    return redirect(url_for('dashboard'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
