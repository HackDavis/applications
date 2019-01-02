import importlib

from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.contrib.google import make_google_blueprint
from flask_login import current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy


class Shared:
    db = None
    google = None
    login_manager = None

    @classmethod
    def instantiate(cls, app):
        """Instantiate shared data"""
        cls.db = SQLAlchemy()
        importlib.import_module('src.models.Answer')
        importlib.import_module('src.models.Application')
        OAuth = importlib.import_module('src.models.OAuth').OAuth
        importlib.import_module('src.models.Question')
        importlib.import_module('src.models.Settings')
        importlib.import_module('src.models.User')
        cls.db.init_app(app)
        with app.app_context():
            cls.db.create_all()

        cls.google = make_google_blueprint(
            client_id=app.config.get('GOOGLE_CLIENT_ID'),
            client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
            scope=app.config.get('GOOGLE_SCOPES'))
        cls.google.backend = SQLAlchemyBackend(OAuth, cls.db.session, user=current_user)
        app.register_blueprint(cls.google)

        cls.login_manager = LoginManager()
        cls.login_manager.init_app(app)
        cls.login_manager.login_view = 'google.login'
        cls.login_manager.session_protection = 'strong'
