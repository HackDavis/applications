from src.shared import Shared
from src.models.lib.ModelUtils import ModelUtils
from src.models.lib.Serializer import Serializer

db = Shared.db

class Settings(db.Model, ModelUtils, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)

    @staticmethod
    def init():
        if len(Settings.get_max_applicants_per_user()) == 0:
            Settings.set_max_applicants_per_user(100)

    @staticmethod
    def get_max_applicants_per_user():
        max_applicants = db.session.query(Settings) \
        .filter(Settings.key == "max_applicants") \
        .all()

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            raise e

        return max_applicants

    @staticmethod
    def set_max_applicants_per_user(new_max):
        max_applicants = db.session.query(Settings) \
        .filter(Settings.key == "max_applicants") \
        .update({'value': new_max})

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            raise e

        return max_applicants

Settings.init()