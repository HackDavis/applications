from flask import abort, request, jsonify, Blueprint, Response
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
import time

from src.models.Answer import Answer
from src.models.schema.Application import Application
from src.models.functions.ApplicationQueries import ApplicationQueries
from src.models.Question import Question
from src.models.Settings import Settings
from src.models.enums.Role import Role
from src.shared import Shared
from src.models.lib.Serializer import Serializer
from src.config.config import Config

from sqlalchemy.orm.session import Session

admin = Blueprint('admin', __name__)

db = Shared.db
google = Shared.google
login_manager = Shared.login_manager


def validate_and_return_string(json, key, is_required):
    """Validate whether value associated with key in json exists (if required value) and is a string"""

    value = json.get(key)  # value could be string, int, etc

    if value is not None:
        if not isinstance(key, str):
            # value is not a string
            abort(400, '{key} not a string'.format(key=key))

        if len(value) == 0:
            # treat empty string as None
            value = None

    if value is None and is_required:
        abort(400, '{key} not provided'.format(key=key))

    return value


def validate_and_return_positive_integer(json, key, is_required):
    """Validate whether value associated with key in json exists (if required value) and is a positive integer"""

    value = json.get(key)  # value could be string, int, etc

    if isinstance(value, str) and len(value) == 0:
        # treat empty string as None
        value = None

    if value is None and is_required:
        abort(400, '{key} not provided'.format(key=key))

    number = None
    if value is not None:
        try:
            # attempt conversion to float
            number_float = float(value)
        except ValueError:
            abort(400, '{key} not an integer'.format(key=key))

        number = int(number_float)
        if number_float != number:
            # number does not cleanly convert to int
            abort(400, '{key} not an integer'.format(key=key))

        if number < 0:
            # number not positive
            abort(400, '{key} not greater than or equal to 0'.format(key=key))

    return number


@admin.route('/api/admin/load', methods=['POST', 'GET'])
@login_required
def load():
    """Reload applications from CSV file."""
    if current_user.role != Role.admin:
        abort(401, 'User needs to be an admin to access this route')

    if 'applicants' not in request.files:
        abort(400, 'No file submitted')
    file = request.files['applicants']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        abort(400, 'Invalid file name')

    filename = secure_filename(file.filename)

    path = os.path.join(Config.UPLOAD_FOLDER, filename)

    file.save(path)

    with open(path, encoding='utf-8') as csv_file:
        # load new rows
        try:
            session = db.session

            start = time.perf_counter()

            question_rows = Question.get_questions_from_db()
            ApplicationQueries.insert_without_duplicates(csv_file, question_rows)

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
        except Exception as e:
            print(e)

@admin.route('/api/admin/reload', methods=['POST'])
@login_required
def reload():
    """Reload applications from CSV file."""
    if current_user.role != Role.admin:
        abort(401, 'User needs to be an admin to access this route')

    if 'applicants' not in request.files:
        abort(400, 'No file submitted')

    file = request.files['applicants']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        abort(400, 'Invalid file name')

    filename = secure_filename(file.filename)

    path = os.path.join(Config.UPLOAD_FOLDER, filename)

    file.save(path)

    with open(path, encoding='utf-8') as csv_file:
        # drop rows
        Answer.drop_rows()
        Application.drop_rows()
        Question.drop_rows()

        # load new rows
        try:
            session = db.session

            start = time.perf_counter()

            question_rows = Question.insert(csv_file, session)
            ApplicationQueries.insert(csv_file, question_rows, session)

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

    ApplicationQueries.standardize_scores()

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

    ranked_users = ApplicationQueries.rank_participants()
    return jsonify(Serializer.serialize_value(ranked_users))


@admin.route('/api/admin/settings', methods=["GET"])
@login_required
def get_settings():
    """Return current settings"""

    if current_user.role != Role.admin:
        abort(401, 'User needs to be an admin to access this route')

    settings = Settings.get_settings()
    if settings is None:
        # no existing settings
        Settings.update_settings()  # insert settings with default values
        settings = Settings.get_settings()

    return jsonify(Serializer.serialize_value(settings))


@admin.route('/api/admin/settings', methods=["PUT"])
@login_required
def update_settings():
    """Validate and persist new settings"""

    if current_user.role != Role.admin:
        abort(401, 'User needs to be an admin to access this route')

    json = request.get_json(force=True)

    # validate values passed in
    name = validate_and_return_string(json, 'name', True)
    application_limit = validate_and_return_positive_integer(json, 'application_limit', False)
    accept_limit = validate_and_return_positive_integer(json, 'accept_limit', True)
    waitlist_limit = validate_and_return_positive_integer(json, 'waitlist_limit', True)

    Settings.update_settings(name, application_limit, accept_limit, waitlist_limit)

    return Response('Updated settings', 200)


@admin.route('/api/admin/demographics', methods=["GET"])
@login_required
def get_demographics():
    """Get the demographic information from applicants"""
    applicant_count = ApplicationQueries.count_accepted()
    answer_totals = ApplicationQueries.count_values_per_answer()

    return jsonify(Serializer.serialize_value({'total': applicant_count, 'answers': answer_totals}))