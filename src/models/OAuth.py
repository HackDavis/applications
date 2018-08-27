from flask_dance.consumer.backend.sqla import OAuthConsumerMixin

from src.shared import Shared
from src.models.lib.Serializer import Serializer
from src.models.User import User

db = Shared.db


class OAuth(OAuthConsumerMixin, db.Model, Serializer):
    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
    last_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
