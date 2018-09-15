import csv

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

    @staticmethod
    def insert(csv_file):
        """Insert new rows extracted from csv_file"""
        questions = Question.get_questions_from_csv(csv_file)
        rows = Question.convert_questions_to_rows(questions)
        Question.insert_rows(rows)
        return rows

    @staticmethod
    def get_questions_from_csv(csv_file):
        """Get questions from CSV file"""
        reader = csv.DictReader(csv_file)
        return reader.fieldnames

    @staticmethod
    def convert_questions_to_rows(questions):
        """Convert questions into rows to insert into database"""
        return [
            # question_tuple[0] is the counter, question_tuple[1] is the question
            Question.convert_question_to_row(question_tuple[0] + 1, question_tuple[1])
            for question_tuple in enumerate(questions)
        ]

    @staticmethod
    def convert_question_to_row(index, question_with_type):
        """Convert question into row to insert into database"""
        question_with_type_list = question_with_type.split('|')
        if len(question_with_type_list) < 2:
            raise ValueError(
                'question or question type not provided for: {question_with_type}'.format(
                    question_with_type=question_with_type))
        elif len(question_with_type_list) > 2:
            raise ValueError(
                'only question and question type should be provided for: {question_with_type}'.
                format(question_with_type=question_with_type))

        raw_question, raw_question_type_string = question_with_type_list
        question = raw_question.strip()
        question_type_string = raw_question_type_string.strip()

        try:
            question_type = QuestionType[question_type_string]
        except KeyError:
            raise ValueError('question type not recognized for: {question_with_type}'.format(
                question_with_type=question_with_type))

        return Question(question=question, question_type=question_type, index=index)
