from src.models.lib.ModelUtils import ModelUtils
from src.models.lib.Serializer import Serializer
from src.shared import Shared

db = Shared.db


class Settings(db.Model, ModelUtils, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    application_limit = db.Column(db.Integer)
    accept_limit = db.Column(db.Integer, nullable=False)
    waitlist_limit = db.Column(db.Integer, nullable=False)
    last_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    @staticmethod
    def get_settings():
        """Retrieve last settings"""

        return db.session.query(Settings) \
            .order_by(Settings.last_modified.desc()) \
            .first()

    @staticmethod
    def update_settings(name="HackDavis",
                        application_limit=None,
                        accept_limit=100,
                        waitlist_limit=100):
        """Insert new settings"""

        settings = Settings(name=name,
                            application_limit=application_limit,
                            accept_limit=accept_limit,
                            waitlist_limit=waitlist_limit)
        Settings.insert_rows([settings])

        return settings
