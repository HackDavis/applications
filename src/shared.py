import importlib

from flask_sqlalchemy import SQLAlchemy
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.contrib.google import make_google_blueprint
from flask_login import current_user, LoginManager


class Shared:
    db = None
    google = None
    login_manager = None

    @classmethod
    def instantiate(cls, app):
        cls.db = SQLAlchemy()
        importlib.import_module('src.models.User')
        importlib.import_module('src.models.Application')
        OAuth = importlib.import_module('src.models.OAuth')
        cls.db.init_app(app)
        with app.app_context():
            cls.db.drop_all()
            cls.db.create_all()

        scopes = 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile'
        cls.google = make_google_blueprint(
            client_id=app.config['GOOGLE_CLIENT_ID'],
            client_secret=app.config['GOOGLE_CLIENT_SECRET'],
            scope=scopes.split(' '))
        cls.google.backend = SQLAlchemyBackend(OAuth.OAuth, cls.db.session, user=current_user)
        app.register_blueprint(cls.google)

        cls.login_manager = LoginManager()
        cls.login_manager.init_app(app)
        cls.login_manager.login_view = "google.login"
        cls.login_manager.session_protection = "strong"
