from src.models.User import User
from src.models.lib.Serializer import Serializer
from src.models.lib.ModelUtils import ModelUtils
from src.shared import Shared

db = Shared.db


class Application(db.Model, ModelUtils, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    locked_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to_user = db.relationship('User', foreign_keys=assigned_to)
    locked_by_user = db.relationship('User', foreign_keys=locked_by)
    score = db.Column(db.Integer, nullable=False)
    standardized_score = db.Column(db.Float)
    feedback = db.Column(db.Text)
    last_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    date_added = db.Column(db.Date, nullable=False)