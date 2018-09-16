import itertools

from src.shared import Shared
from src.models.lib.ModelUtils import ModelUtils
from src.models.lib.Serializer import Serializer
from src.models.enums.QuestionType import QuestionType
from src.models.Question import Question

db = Shared.db


class Answer(db.Model, ModelUtils, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        db.Integer, db.ForeignKey('application.id'), nullable=False, index=True)
    application = db.relationship('Application', foreign_keys=application_id)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    question = db.relationship('Question', foreign_keys=question_id)
    answer = db.Column(db.Text, nullable=False)
    last_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    @staticmethod
    def insert(question_rows, applications, application_rows):
        """Insert new rows extracted from CSV file"""
        rows = Answer.convert_applications_to_rows(question_rows, applications, application_rows)
        Answer.insert_rows(rows)
        return rows

    @staticmethod
    def convert_applications_to_rows(question_rows, applications, application_rows):
        """Convert applications into rows to insert into database"""
        rows = list(map(lambda application, application_row: Answer.convert_application_to_rows(question_rows, application, application_row), applications, application_rows))
        return list(itertools.chain(*rows))

    @staticmethod
    def convert_application_to_rows(question_rows, application, application_row):
        """Convert one application into rows to insert into database"""
        answers = Answer.get_answers_from_application(application)
        return list(map(lambda question_row, answer: Answer(application_id=application_row.id, question_id=question_row.id, answer=answer), question_rows, answers))

    @staticmethod
    def get_answers_from_application(application):
        """Get answers from one application"""
        return application

    @staticmethod
    def get_answers(application_id):
        """Returns all answers associated with the application ID"""
        m_list = db.session.query(Answer) \
        .filter(Answer.application_id == application_id) \
        .join(Question) \
        .filter(Question.question_type != QuestionType.ignore) \
        .with_entities(Question.question, Question.question_type, Answer.answer) \
        .all()

        return [{"answer": row[2], "question": {"question": row[0], "question_type": row[1]}} for row in m_list]
