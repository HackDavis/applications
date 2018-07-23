from flask_login import UserMixin

from src.shared import Shared
from src.models.enums.Role import Role

db = Shared.db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(256))
    last_name = db.Column(db.String(256))
    picture = db.Column(db.String(256))
    role = db.Column(db.Enum(Role), nullable=False)
