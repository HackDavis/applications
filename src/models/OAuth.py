from flask_dance.consumer.backend.sqla import OAuthConsumerMixin

from src.shared import Shared
from src.models.User import User

db = Shared.db


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
