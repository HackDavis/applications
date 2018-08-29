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
    def convert_question_to_row(index, question):
        """Convert question into row to insert into database"""
        return Question(question=question, question_type=QuestionType.essay, index=index)
