from flask import abort, request, jsonify, Blueprint, Response
from flask_login import current_user, login_required
import os
import time

from src.models.Answer import Answer
from src.models.Application import Application
from src.models.Question import Question
from src.models.enums.Role import Role
from src.shared import Shared
from src.models.lib.Serializer import Serializer

from sqlalchemy.orm.session import Session

admin = Blueprint('admin', __name__)

db = Shared.db
google = Shared.google
login_manager = Shared.login_manager


@admin.route('/api/admin/reload', methods=['POST', 'GET'])
@login_required
def reload():
    """Reload applications from CSV file."""
    if current_user.role != Role.admin:
        abort(401, 'User needs to be an admin to access this route')

    with open(os.path.join(os.getcwd(), 'sample.csv'), encoding='utf-8') as csv_file:
        # drop rows
        Answer.drop_rows()
        Application.drop_rows()
        Question.drop_rows()

        # load new rows
        try:
            session = db.session

            start = time.perf_counter()

            question_rows = Question.insert(csv_file, session)
            Application.insert(csv_file, question_rows, session)

            op_time = time.perf_counter()

            print("Total insert time", op_time - start)

            try:
                session.commit()
                
                commit_time = time.perf_counter()
                print("Commit time", commit_time - op_time)

            except Exception as e:
                session.rollback()
                print(e)
                raise(e)

            return Response('Reloaded applications from CSV file', 200)
        except ValueError as e:
            abort(400, str(e))


@admin.route('/api/admin/standardize', methods=['POST', 'GET'])
@login_required
def standardize():
    """Calculate and persist standardized scores."""
    if current_user.role != Role.admin:
        abort(401, 'User needs to be an admin to access this route')

    Application.standardize_scores()

    return Response('Standardized scores', 200)

@admin.route('/api/admin/configure', methods=["GET"])
@login_required
def configure_parameters():
    if current_user.role != Role.admin:
        abort(401, 'User needs to be an admin to access this route')

    res = {}
    res["question_weights"] = Question.get_question_weights()
    res["answer_weights"] = Answer.get_unique_answer_weights()

    return jsonify(Serializer.serialize_value(res))

@admin.route('/api/admin/configure', methods=["PUT"])
@login_required
def update_parameters():
    if current_user.role != Role.admin:
        abort(401, 'User needs to be an admin to access this route')
    
    data = request.get_json()
    Question.update_question_weights(data['question_weights'])
    Answer.set_unique_answer_weights(data["answer_weights"])

    return Response('Updated scores', 200)

@admin.route("/api/admin/rank", methods=["GET"])
@login_required
def get_final_acceptance_list():
    if current_user.role != Role.admin:
        abort(401, 'User needs to be an admin to access this route')

    ranked_users = Application.rank_participants()
    return jsonify(Serializer.serialize_value(ranked_users))
