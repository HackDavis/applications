from src.models.enums.ActionType import ActionType
from src.models.lib.ModelUtils import ModelUtils
from src.models.lib.Serializer import Serializer
from src.shared import Shared

db = Shared.db


class Action(db.Model, ModelUtils, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    action_type = db.Column(db.Enum(ActionType), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', foreign_keys=user_id)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    application = db.relationship('Application', foreign_keys=application_id)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    @staticmethod
    def log_action(action_type, user_id, application_id=None):
        """Log action"""

        action = Action(action_type=action_type, user_id=user_id, application_id=application_id)
        Action.insert_rows([action])

        return action
