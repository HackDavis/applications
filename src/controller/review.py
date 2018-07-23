from flask import Blueprint, current_app, flash, redirect, url_for
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import login_required, login_user, logout_user
from sqlalchemy.orm.exc import NoResultFound
import os

from src.shared import Shared
from src.models.User import User
from src.models.OAuth import OAuth
from src.models.enums.Role import Role

review = Blueprint('review', __name__)

db = Shared.db
google = Shared.google
login_manager = Shared.login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# create/login local user on successful OAuth login
@oauth_authorized.connect_via(google)
def google_logged_in(google, token):
    if not token:
        flash('Failed to log in with Google.', category='error')
        return False
    resp = google.session.get(current_app.config['GOOGLE_USER_INFO_PATH'])
    if not resp.ok:
        flash("Failed to fetch user info from Google.", category="error")
        return False

    google_info = resp.json()

    if not google_info['hd'] or google_info['hd'] != current_app.config['DOMAIN']:
        flash("User not in domain", category="error")
        return False

    google_user_id = str(google_info["id"])

    # find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=google.name,
        provider_user_id=google_user_id,
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=google.name,
            provider_user_id=google_user_id,
            token=token,
        )

    if oauth.user:
        # TODO: update user row with new information if applicable
        login_user(oauth.user)
    else:
        # create a new local user account for this user
        user = User(
            email=google_info['email'],
            first_name=google_info['given_name'],
            last_name=google_info['family_name'],
            picture=google_info['picture'],
            role=Role.user)
        # associate the new local user account with the OAuth token
        oauth.user = user
        # save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # login the new local user account
        login_user(user)

    flash("Successfully signed in with Google.")
    # disable Flask-Dance's default behavior for saving the OAuth token
    return False


# notify on OAuth provider error
@oauth_error.connect_via(google)
def google_error(google, error, error_description=None, error_uri=None):
    msg = ("OAuth error from {name}! "
           "error={error} description={description} uri={uri}").format(
               name=google.name,
               error=error,
               description=error_description,
               uri=error_uri,
           )
    flash(msg, category="error")


@review.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("google.login"))


@review.route('/configure/upload_csv')
@login_required
def doCSV():
    """Upload CSV file."""
    with open(os.path.join(_dirname, "../lib/sample.csv"), encoding="utf-8") as data:
        loadCSV.upload_csv(data)
    return Response(status=201)
