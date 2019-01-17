import csv
import time

from src.shared import Shared
from src.models.enums.QuestionType import QuestionType
from src.models.lib.ModelUtils import ModelUtils
from src.models.lib.Serializer import Serializer

from sqlalchemy.sql.expression import func

db = Shared.db


class Question(db.Model, ModelUtils, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.Enum(QuestionType), nullable=False)
    index = db.Column(db.Integer, nullable=False, unique=True, index=True)
    last_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    weight = db.Column(db.Float)

    @staticmethod
    def insert(csv_file):
        """Insert new rows extracted from csv_file"""

        start = time.perf_counter()

        questions = Question.get_questions_from_csv(csv_file)
        question_types = Question.get_question_types_from_csv(csv_file)
        rows = Question.convert_questions_to_rows(questions, question_types)

        object_time = time.perf_counter()

        print("question load time: ", object_time - start)

        db.session.bulk_save_objects(rows, return_defaults=True)

        question_bulk_save_time = time.perf_counter()

        print("question save time: ", question_bulk_save_time - object_time)
        return rows

    @staticmethod
    def get_questions_from_db():
        return db.session.query(Question).all()

    @staticmethod
    def get_questions_from_csv(csv_file):
        """Get questions from CSV file"""
        reader = csv.DictReader(csv_file)
        return reader.fieldnames

    @staticmethod
    def get_question_types_from_csv(csv_file):
        """Get question types from CSV file"""
        reader = csv.reader(csv_file)
        return next(reader)

    @staticmethod
    def convert_questions_to_rows(questions, question_types):
        """Convert questions into rows to insert into database"""
        # question_tuple[0] is the counter, question_tuple[1] is the question
        return list(map(lambda question_tuple, question_type: Question.convert_question_to_row(question_tuple[0] + 1, question_tuple[1], question_type), enumerate(questions), question_types))

    @staticmethod
    def convert_question_to_row(index, raw_question, raw_question_type_string):
        """Convert question into row to insert into database"""
        question = raw_question.strip()
        question_type_string = raw_question_type_string.strip()

        try:
            question_type = QuestionType[question_type_string]
        except KeyError:
            raise ValueError(
                'question type {question_type} not recognized for question: {question}'.format(
                    question_type=question_type_string, question=question))

        return Question(question=question, question_type=question_type, index=index, weight=0)

    @staticmethod
    def get_question_weights():
        weights = db.session.query(Question.id, Question.question, Question.weight) \
        .filter((Question.question_type == QuestionType.demographic) | (Question.question_type == QuestionType.university)) \
        .all()
        return weights
    
    @staticmethod
    def get_row_for_question(index, question, question_type):
        row = db.session.query(Question).filter((Question.question == question) | (Question.index == index)).first()
        if row is None:
            row = Question.convert_question_to_row(index, question, question_type)
            Question.insert_rows([row])

        return row

    @staticmethod
    def map_questions_to_question_rows(questions, question_types):
        return list(map(lambda question_tuple, question_type: Question.get_row_for_question(question_tuple[0] + 1, question_tuple[1], question_type), enumerate(questions), question_types))

    @staticmethod
    def update_question_weights(question_weights):
        for weight in question_weights:
            db.session.query(Question) \
            .filter(Question.id == weight[0]) \
            .update({"weight": weight[2]})
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)