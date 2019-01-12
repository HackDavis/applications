import itertools
import time

from src.shared import Shared
from src.models.lib.ModelUtils import ModelUtils
from src.models.lib.Serializer import Serializer
from src.models.enums.QuestionType import QuestionType
from src.models.Question import Question

from sqlalchemy.sql.expression import func

db = Shared.db


class Answer(db.Model, ModelUtils, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        db.Integer, db.ForeignKey('application.id'), nullable=False, index=True)
    application = db.relationship('Application', foreign_keys=application_id)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False, index=True)
    question = db.relationship('Question', foreign_keys=question_id)
    answer_weight = db.Column(db.Float, default=1)
    answer = db.Column(db.Text, nullable=False)
    last_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    @staticmethod
    def insert(question_rows, applications, application_rows):
        """Insert new rows extracted from CSV file"""

        start = time.perf_counter()

        rows = Answer.convert_applications_to_rows(question_rows, applications, application_rows)

        object_load = time.perf_counter()
        print("Answers load time", object_load - start)

        db.session.bulk_save_objects(rows)

        bulk_save = time.perf_counter()
        print("Answers save time", bulk_save - object_load)
        return rows

    @staticmethod
    def check_duplicate_email(email):
        is_duplicate = db.session.query(Answer) \
        .join(Question) \
        .filter(Question.question_type == QuestionType.email, Answer.answer == email) \
        .first()
        if is_duplicate is not None:
            return is_duplicate
        
        return None

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
        answers = db.session.query(Answer) \
            .filter(Answer.application_id == application_id) \
            .join(Question) \
            .filter(Question.question_type != QuestionType.ignore) \
            .with_entities(Question.question, Question.question_type, Answer.answer) \
            .all()

        return [{
            "answer": row[2],
            "question": {
                "question": row[0],
                "question_type": row[1]
            }
        } for row in answers]

    @staticmethod
    def get_identifying_answers(application_id):
        """Returns answers associated with the application ID that are deemed important for quick identification"""
        answers = db.session.query(Answer) \
            .filter(Answer.application_id == application_id) \
            .join(Question) \
            .filter((Question.question_type == QuestionType.firstName) | (Question.question_type == QuestionType.lastName) | (Question.question_type == QuestionType.email) | (Question.question_type == QuestionType.university)) \
            .with_entities(Question.question, Question.question_type, Answer.answer) \
            .all()

        return [{
            "answer": row[2],
            "question": {
                "question": row[0],
                "question_type": row[1]
            }
        } for row in answers]

    @staticmethod
    def get_unique_answer_weights():
        question_answer = db.session.query(Answer.question_id, Answer.answer, Answer.answer_weight) \
        .distinct(Answer.answer, Answer.question_id) \
        .join(Question) \
        .filter((Question.question_type == QuestionType.demographic) | (Question.question_type == QuestionType.university)) \
        .add_column(Question.question) \
        .add_column(Question.id) \
        .from_self(Question.id, Question.question, func.array_agg(Answer.answer), func.array_agg(Answer.answer_weight)) \
        .group_by(Question.id, Question.question)

        results = question_answer.all()
        transformed = []

        for result in results:
            t = [result[0], result[1]]
            weights = [{"name": k, "weight": v} for k, v in zip(result[2], result[3])]
            t.append(weights)
            transformed.append(t)

        print(len(transformed))

        return transformed
    
    @staticmethod
    def set_unique_answer_weights(answer_weights):
        for question in answer_weights:
            for weight in question[2]:
                db.session.query(Answer) \
                .filter(Answer.question_id == question[0], Answer.answer == weight["name"]) \
                .update({"answer_weight": weight["weight"]})
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
    