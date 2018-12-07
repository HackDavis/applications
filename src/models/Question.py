import csv
import time

from src.shared import Shared
from src.models.enums.QuestionType import QuestionType
from src.models.lib.ModelUtils import ModelUtils
from src.models.lib.Serializer import Serializer

db = Shared.db


class Question(db.Model, ModelUtils, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(256), nullable=False)
    question_type = db.Column(db.Enum(QuestionType), nullable=False)
    index = db.Column(db.Integer, nullable=False, unique=True, index=True)
    last_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    weight = db.Column(db.FLOAT)

    @staticmethod
    def insert(csv_file, session):
        """Insert new rows extracted from csv_file"""

        start = time.perf_counter()

        questions = Question.get_questions_from_csv(csv_file)
        question_types = Question.get_question_types_from_csv(csv_file)
        rows = Question.convert_questions_to_rows(questions, question_types)

        object_time = time.perf_counter()

        print("question load time: ", object_time - start)

        session.bulk_save_objects(rows, return_defaults=True)

        question_bulk_save_time = time.perf_counter()

        print("question save time: ", question_bulk_save_time - object_time)
        return rows

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

        return Question(question=question, question_type=question_type, index=index)
