from flask import abort, Blueprint, current_app, redirect, url_for, request, session
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import login_required, login_user, logout_user
from sqlalchemy.orm.exc import NoResultFound

from src.models.OAuth import OAuth
from src.models.User import User
from src.models.enums.Role import Role
from src.shared import Shared

import os

auth = Blueprint('auth', __name__)

db = Shared.db
google = Shared.google
login_manager = Shared.login_manager


@login_manager.user_loader
def load_user(user_id):
    """Return current user info"""
    try:
        return db.session.query(User).filter(User.id == user_id).one()
    except NoResultFound:
        return None


@oauth_authorized.connect_via(google)
def google_logged_in(google, token):
    """Create/login local user on successful OAuth login"""
    if not token:
        abort(503, 'Failed to login with Google')

    resp = google.session.get(current_app.config.get('GOOGLE_USER_INFO_PATH'))
    if not resp.ok:
        abort(503, 'Failed to fetch user info from Google.')

    google_info = resp.json()

    if not google_info.get('hd') or google_info.get('hd') != current_app.config.get('DOMAIN'):
        abort(401, 'User not in domain')

    google_user_id = str(google_info.get('id'))

    try:
        # find the OAuth object in the database if it exists
        oauth = db.session.query(OAuth)\
            .filter((OAuth.provider == google.name) & (OAuth.provider_user_id == google_user_id))\
            .one()
    except NoResultFound:
        # create OAuth object
        oauth = OAuth(provider=google.name, provider_user_id=google_user_id, token=token)

    if oauth.user:
        user = oauth.user
    else:
        # create a new user account for this user
        user = User(role=Role.user)
        # associate the new user account with the OAuth object
        oauth.user = user
        db.session.add_all([oauth, user])

    # load updated info
    user.email = google_info.get('email'),
    user.first_name = google_info.get('given_name'),
    user.last_name = google_info.get('family_name'),
    user.picture = google_info.get('picture'),

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, 'Failed to persist user.')

    # login the user account
    login_user(user, remember=True)

    redirect_url = session.get('next')
    print(redirect_url)

    if redirect_url is not None:
        session['next'] = None
        if os.environ.get('FLASK_ENV') == "development":
            redirect_url = "http://localhost:8080" + redirect_url
        return redirect(redirect_url)

    # disable Flask-Dance's default behavior for saving the OAuth token
    return False


@oauth_error.connect_via(google)
def google_error(google, error, error_description=None, error_uri=None):
    """Callback for Google error"""
    message = 'OAuth error from Google! error={error} description={description} uri={uri}'.format(
        error=error,
        description=error_description,
        uri=error_uri,
    )
    abort(503, message)


@auth.route('/login', methods=['GET'])
def login():
    redirect_url = request.args.get('next')
    if redirect_url is not None:
        session['next'] = redirect_url

    return redirect(url_for('google.login'))


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    """Logout user"""
    logout_user()
    return redirect("/")
