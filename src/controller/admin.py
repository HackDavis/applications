from flask import abort, Blueprint, Response
from flask_login import login_required
import os

from src.models.Answer import Answer
from src.models.Application import Application
from src.models.Question import Question
from src.shared import Shared

admin = Blueprint('admin', __name__)

db = Shared.db
google = Shared.google
login_manager = Shared.login_manager


@admin.route('/api/admin/reload', methods=['POST', 'GET'])
@login_required
def reload():
    """Reload applications from CSV file."""
    with open(os.path.join(os.getcwd(), 'sample.csv'), encoding='utf-8') as csv_file:
        # drop rows
        Answer.drop_rows()
        Application.drop_rows()
        Question.drop_rows()

        # load new rows
        try:
            question_rows = Question.insert(csv_file)
            Application.insert(csv_file, question_rows)
            return Response('Reloaded applications from CSV file', 200)
        except ValueError as e:
            abort(400, str(e))
