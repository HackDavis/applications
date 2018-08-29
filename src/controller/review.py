from flask import abort, Blueprint, jsonify, request, Response
from flask_login import current_user, login_required

from src.models.Answer import Answer
from src.models.Application import Application
from src.models.lib.Serializer import Serializer
from src.shared import Shared

review = Blueprint('review', __name__)

db = Shared.db
google = Shared.google
login_manager = Shared.login_manager


@review.route('/review', methods=['GET'])
@login_required
def get_application():
    """Get application for user"""
    application = Application.get_application(current_user.get_id())
    if application is None:
        return Response('No more applications left to score', 200)

    answers = Answer.get_answers(application.id)
    response = {'application': application, 'answers': answers}
    return jsonify(Serializer.serialize_value(response))


@review.route('/review/skip', methods=['GET'])
@login_required
def skip_application():
    """Skip application for user"""
    past_application = Application.skip_application(current_user.get_id())
    if past_application is None:
        abort(400, 'User is not currently assigned an application')

    application = Application.get_application(current_user.get_id())
    if application is None:
        return Response('No more applications left to score', 200)

    answers = Answer.get_answers(application.id)
    response = {'application': application, 'answers': answers}
    return jsonify(Serializer.serialize_value(response))


@review.route('/review/score', methods=['POST'])
@login_required
def score_application():
    """Score application"""
    score_str = request.args.get('score')
    if score_str is None:
        abort(400, 'score not provided')

    try:
        score = int(score_str)
    except ValueError:
        abort(400, 'score not an integer')

    if score < 1 or score > 5:
        abort(400, 'score not between 1 and 5')

    application = Application.update_score(current_user.get_id(), score)
    if application is None:
        abort(400, 'User is not currently assigned an application')

    return Response('Updated score for application', 200)
