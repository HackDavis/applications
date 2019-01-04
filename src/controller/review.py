from flask import abort, Blueprint, jsonify, request, Response
from flask_login import current_user, login_required

from src.models.Answer import Answer
from src.models.Application import Application
from src.models.Settings import Settings
from src.models.enums.Role import Role
from src.models.lib.Serializer import Serializer
from src.shared import Shared

review = Blueprint('review', __name__)

db = Shared.db
google = Shared.google
login_manager = Shared.login_manager


def is_authorized(application, is_read_only):
    if current_user.role == Role.admin:
        # admins are authorized for any application
        return True

    if application is not None and application.assigned_to == current_user.id and application.score != 0 and (
            is_read_only or application.locked_by is None):
        # authorized if application is assigned to user, has been rated, and either is a read only operation or is not locked by an admin
        return True

    currently_assigned_application = Application.get_currently_assigned_application_for_user(
        current_user.id)
    if currently_assigned_application is not None and currently_assigned_application.id == application.id:
        # authorized if application is the one currently assigned to user
        return True

    return False


@review.route('/api/review', methods=['GET'])
@login_required
def get_application():
    """Get application for user"""
    if current_user.role != Role.admin:
        settings = Settings.get_settings()
        application_count = Application.get_count_of_applications_for_user(current_user.id)
        if application_count >= settings.application_limit:
            # no more applications to score for user
            return Response(status=204)

    application = Application.get_application_for_user(current_user.id)
    if application is None:
        # no more applications to score
        return Response(status=204)

    answers = Answer.get_answers(application.id)
    response = {'application': application, 'answers': answers}
    return jsonify(Serializer.serialize_value(response))


@review.route('/api/review/<application_id_str>', methods=['GET'])
@login_required
def get_application_using_id(application_id_str):
    """Get application associated with application ID"""
    try:
        application_id = int(application_id_str)
    except ValueError:
        abort(400, 'application ID invalid')

    application = Application.get_application(application_id)
    if application is None:
        abort(404, 'Application does not exist')
    elif not is_authorized(application, True):
        abort(401, 'User is not authorized for this application')

    answers = Answer.get_answers(application.id)
    response = {'application': application, 'answers': answers}
    return jsonify(Serializer.serialize_value(response))


@review.route('/api/review/skip', methods=['GET'])
@login_required
def skip_application():
    """Skip application for user"""
    past_application = Application.skip_application(current_user.id)
    if past_application is None:
        abort(400, 'User is not currently assigned an application')

    return get_application()


@review.route('/api/review/<application_id_str>/score', methods=['POST'])
@login_required
def score_application(application_id_str):
    """Score application"""
    try:
        application_id = int(application_id_str)
    except ValueError:
        abort(400, 'application ID invalid')

    application = Application.get_application(application_id)
    if application is None:
        abort(404, 'Application does not exist')
    elif not is_authorized(application, False):
        abort(401, 'User is not authorized for this application')

    json = request.get_json(force=True)

    score_str = json.get('score')
    feedback = json.get('feedback')

    if score_str is None:
        abort(400, 'score not provided')

    try:
        score = int(score_str)
    except ValueError:
        abort(400, 'score not an integer')

    if score < 1 or score > 5:
        abort(400, 'score not between 1 and 5')

    locked_by = None
    if current_user.role == Role.admin:
        locked_by = current_user.id

    Application.update_score_and_feedback(application, score, feedback, locked_by)

    return Response('Updated score for application', 200)
