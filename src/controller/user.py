from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from src.models.Answer import Answer
from src.models.Application import Application
from src.models.enums.Role import Role
from src.models.lib.Serializer import Serializer
from src.shared import Shared

user = Blueprint('user', __name__)

db = Shared.db
google = Shared.google
login_manager = Shared.login_manager


@user.route('/api/user', methods=['GET'])
@login_required
def get_user():
    """Get information about the user"""
    return jsonify(Serializer.serialize_value(current_user._get_current_object()))


@user.route('/api/user/scores', methods=['GET'])
@login_required
def get_scores():
    """Get scores and other information about the applications the user is authorized for"""
    if current_user.role == Role.admin:
        applications = Application.get_all_applications()
    else:
        applications = Application.get_all_applications_for_user(current_user.id)

    response = [{
        'application': application,
        'answers': Answer.get_identifying_answers(application.id)
    } for application in applications]
    return jsonify(Serializer.serialize_value(response))
