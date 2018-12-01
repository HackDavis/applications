from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from src.models.Answer import Answer
from src.models.Application import Application
from src.models.Question import Question
from src.models.enums.QuestionType import QuestionType
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

    app = applications.subquery()

    firstNames = db.session.query(Answer).join(Question).filter(Question.question_type == QuestionType.firstName).subquery()
    lastNames = db.session.query(Answer).join(Question).filter(Question.question_type == QuestionType.lastName).subquery()
    emails = db.session.query(Answer).join(Question).filter(Question.question_type == QuestionType.email).subquery()
    universities = db.session.query(Answer).join(Question).filter(Question.question_type == QuestionType.university).subquery()

    response = db.session.query(Application.id, Application.score, firstNames.c.answer, lastNames.c.answer, emails.c.answer, universities.c.answer).join(app, app.c.id == Application.id) \
    .join(firstNames, firstNames.c.application_id == Application.id) \
    .join(lastNames, lastNames.c.application_id == Application.id) \
    .join(emails, emails.c.application_id == Application.id) \
    .join(universities, universities.c.application_id == Application.id) \
    
    my_results = [{'id': row[0], 'score': row[1], 'firstName': row[2], 'lastName': row[3], 'email': row[4], 'university': row[5]} for row in response.all()]

    return jsonify(my_results)
