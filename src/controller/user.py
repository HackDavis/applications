from flask import Blueprint, jsonify
from flask_login import current_user, login_required
from datetime import datetime, timedelta, date

from sqlalchemy.orm import aliased
from sqlalchemy.sql.functions import func

from src.models.Answer import Answer
from src.models.Application import Application
from src.models.Question import Question
from src.models.User import User
from src.models.Settings import Settings
from src.models.enums.QuestionType import QuestionType
from src.models.enums.Role import Role
from src.models.lib.Serializer import Serializer
from src.shared import Shared

# import time

user = Blueprint('user', __name__)

db = Shared.db
google = Shared.google
login_manager = Shared.login_manager


@user.route('/api/user', methods=['GET'])
@login_required
def get_user():
    """Get information about the user"""
    return jsonify(Serializer.serialize_value(current_user._get_current_object()))


@user.route('/api/user/progress', methods=['GET'])
@login_required
def get_progress():
    team_total = Application.count_applications()
    team_scored = Application.count_scored()

    user_total = Settings.get_settings().application_limit

    if user_total is None:
        user_total = team_total / User.count_users()

    user_scored = db.session.query(Application) \
    .filter(Application.assigned_to == current_user.id, Application.score != 0) \
    .count()

    return jsonify(Serializer.serialize_value({'team': {'done': team_scored, 'total': team_total}, 'self': {'done': user_scored, 'total': user_total}}))

@user.route('/api/user/scores', methods=['GET'])
@login_required
def get_scores():
    """Get scores and other information about the applications the user is authorized for"""

    # start = time.perf_counter()

    if current_user.role == Role.admin:
        applications = Application.get_all_applications()
    else:
        applications = Application.get_all_applications_for_user(current_user.id)

    app = applications.subquery()

    cutoff = datetime.now() - timedelta(hours=1)

    assigned_to_user = aliased(User)
    locked_by_user = aliased(User)
    response = db.session.query(Application.id, Application.score, assigned_to_user.email, locked_by_user.email, func.json_object_agg(Question.question_type, Answer.answer)) \
        .order_by(Application.last_modified.desc()) \
        .filter(Application.id == app.c.id) \
        .join(assigned_to_user, (Application.assigned_to == assigned_to_user.id) & ((Application.score != 0) | (Application.last_modified > cutoff)), isouter=True) \
        .join(locked_by_user, Application.locked_by_user, isouter=True) \
        .join(Answer) \
        .join(Question) \
        .filter((Question.question_type == QuestionType.email)
                | (Question.question_type == QuestionType.firstName)
                | (Question.question_type == QuestionType.lastName)
                | (Question.question_type == QuestionType.university)) \
        .group_by(Application.id, assigned_to_user.email, locked_by_user.email) \
        .all()

    # firstNames = db.session.query(Answer).join(Question).filter(Question.question_type == QuestionType.firstName).subquery()
    # lastNames = db.session.query(Answer).join(Question).filter(Question.question_type == QuestionType.lastName).subquery()
    # emails = db.session.query(Answer).join(Question).filter(Question.question_type == QuestionType.email).subquery()
    # universities = db.session.query(Answer).join(Question).filter(Question.question_type == QuestionType.university).subquery()

    # response = db.session.query(Application.id, Application.score, firstNames.c.answer, lastNames.c.answer, emails.c.answer, universities.c.answer).join(app, app.c.id == Application.id) \
    # .join(firstNames, firstNames.c.application_id == Application.id) \
    # .join(lastNames, lastNames.c.application_id == Application.id) \
    # .join(emails, emails.c.application_id == Application.id) \
    # .join(universities, universities.c.application_id == Application.id) \
    # .all()

    # t2 = time.perf_counter()

    #my_results = []
    #cur_row = {}
    #cur_row["id"] = response[0][0]

    #for row in response:
    #    if row[0] != cur_row["id"]:
    #        my_results.append(cur_row)
    #        cur_row = {}
    #        cur_row["id"] = int(row[0])
#
    #    cur_row["score"] = int(row[1])
    #    cur_row[row[3].name] = row[2]

    # my_results = [{'id': row[0], 'score': row[1], 'firstName': row[2], 'lastName': row[3], 'email': row[4], 'university': row[5]} for row in response]

    my_results = [{
        'id': row[0],
        'score': row[1],
        'assignedToEmail': row[2],
        'lockedByEmail': row[3],
        'university': row[4]['university'],
        'email': row[4]['email'],
        'firstName': row[4]['firstName'],
        'lastName': row[4]['lastName']
    } for row in response]

    # t3 = time.perf_counter()

    # print("t3 - t2", t3 - t2)
    # print("t2 - start", t2 - start)

    return jsonify(my_results)
