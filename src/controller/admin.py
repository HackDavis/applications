from flask import abort, request, jsonify, Blueprint, Response, stream_with_context
from flask_login import current_user, login_required
from functools import reduce
from io import StringIO
from werkzeug.utils import secure_filename
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response
from datetime import datetime
import csv
import os
import time

from src.models.Action import Action
from src.models.Answer import Answer
from src.models.Application import Application
from src.models.Question import Question
from src.models.Settings import Settings
from src.models.enums.QuestionType import QuestionType
from src.models.enums.ActionType import ActionType
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
            start = time.perf_counter()

            csv_questions = Question.get_questions_from_csv(csv_file) # need to advance the csv_file reader
            question_rows = Question.map_questions_to_question_rows(csv_questions)
            
            Application.insert(csv_file, question_rows, True)

            op_time = time.perf_counter()
            print("Total insert time", op_time - start)

            Action.log_action(ActionType.load, current_user.id)

            return Response('Reloaded applications from CSV file', 200)
        except ValueError as e:
            abort(400, str(e))


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
        Action.drop_rows()
        Answer.drop_rows()
        Application.drop_rows()
        Question.drop_rows()

        # load new rows
        try:
            start = time.perf_counter()

            question_rows = Question.insert(csv_file)
            Application.insert(csv_file, question_rows, False)

            op_time = time.perf_counter()
            print("Total insert time", op_time - start)

            Action.log_action(ActionType.reload, current_user.id)

            return Response('Reloaded applications from CSV file', 200)
        except ValueError as e:
            abort(400, str(e))


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

    Action.log_action(ActionType.configure_weights, current_user.id)

    return Response('Updated scores', 200)


def generate_csv(ranked_applications):
    data = StringIO()
    writer = csv.writer(data)

    if len(ranked_applications) == 0:
        writer.writerow('No applications scored')
        return data.getvalue()

    settings = Settings.get_settings()

    first = ranked_applications[0]
    questions = sorted(first[1].keys())

    # write header
    headers = questions + ['score', 'result']
    writer.writerow(headers)
    yield data.getvalue()
    data.seek(0)
    data.truncate(0)

    # write each application
    for rank in range(len(ranked_applications)):
        application = ranked_applications[rank]

        result = 'REJECT'
        if rank + 1 < settings.accept_limit:
            result = 'ACCEPT'
        elif rank + 1 < settings.accept_limit + settings.waitlist_limit:
            result = 'WAITLIST'

        answers = [value for (key, value) in sorted(application[1].items())]
        row = answers + [application[2], result]
        writer.writerow(row)
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)


@admin.route("/api/admin/export", methods=["GET"])
@login_required
def export():
    if current_user.role != Role.admin:
        abort(401, 'User needs to be an admin to access this route')

    ranked_applications = Application.rank_participants()

    Action.log_action(ActionType.export, current_user.id)

    headers = Headers()
    headers.set('Content-Disposition', 'attachment', filename='export.csv')

    # stream the response as the data is generated
    return Response(stream_with_context(generate_csv(ranked_applications)), mimetype='text/csv', headers=headers)


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

    Action.log_action(ActionType.configure_settings, current_user.id)

    return Response('Updated settings', 200)


@admin.route('/api/admin/demographics', methods=["GET"])
@login_required
def get_demographics():
    """Get the demographic information from applicants"""
    applicant_count = Application.count_accepted()
    answer_totals = Application.count_values_per_answer()

    return jsonify(Serializer.serialize_value({'total': applicant_count, 'answers': answer_totals}))