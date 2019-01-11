from flask_login import UserMixin

from src.shared import Shared
from src.models.enums.Role import Role
from src.models.lib.Serializer import Serializer

db = Shared.db


class User(db.Model, UserMixin, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(256))
    last_name = db.Column(db.String(256))
    picture = db.Column(db.String(256))
    role = db.Column(db.Enum(Role), nullable=False)
    last_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    @staticmethod
    def count_users():
        return db.session.query(User).count()
