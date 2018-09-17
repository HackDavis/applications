import csv
from datetime import datetime, timedelta
from sqlalchemy.sql.expression import func

from src.shared import Shared
from src.models.Answer import Answer
from src.models.lib.ModelUtils import ModelUtils
from src.models.lib.Serializer import Serializer

db = Shared.db


class Application(db.Model, ModelUtils, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    scoring_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    user = db.relationship('User', foreign_keys=scoring_user_id)
    score = db.Column(db.Integer, nullable=False)
    last_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    @staticmethod
    def insert(csv_file, question_rows):
        """Insert new rows extracted from csv_file"""
        applications = Application.get_applications_from_csv(csv_file)
        rows = Application.convert_applications_to_rows(applications)
        Application.insert_rows(rows)
        Answer.insert(question_rows, applications, rows)
        return rows

    @staticmethod
    def get_applications_from_csv(csv_file):
        """Get applications from CSV file"""
        applications = list(csv.reader(csv_file))
        return applications[1:]

    @staticmethod
    def convert_applications_to_rows(applications):
        """Convert applications into rows to insert into database"""
        return [Application.convert_application_to_row(application) for application in applications]

    @staticmethod
    def convert_application_to_row(application):
        """Convert application into row to insert into database"""
        return Application(score=0)

    @staticmethod
    def get_existing_application(user_id):
        """Returns application associated with user ID"""
        cutoff = datetime.now() - timedelta(hours=1)
        return db.session.query(Application)\
            .filter((Application.scoring_user_id == user_id) & (Application.last_modified > cutoff))\
            .first()

    @staticmethod
    def get_application(user_id):
        """Returns application for user to review"""
        application = Application.get_existing_application(user_id)
        if application is None:
            cutoff = datetime.now() - timedelta(hours=1)
            application = db.session.query(Application)\
                .filter((Application.scoring_user_id == None) | (Application.last_modified < cutoff)) \
                .limit(50) \
                .from_self() \
                .order_by(func.random()) \
                .first()

            if application is None:
                return None

            application.scoring_user_id = user_id

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

        return application

    @staticmethod
    def skip_application(user_id):
        """Returns next application for user to review"""
        application = Application.get_existing_application(user_id)

        if application is None:
            return None

        application.scoring_user_id = None

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

        return application

    @staticmethod
    def update_score(user_id, score):
        """Updates the score for an application"""
        application = Application.get_existing_application(user_id)

        if application is None:
            return None

        application.scoring_user_id = None
        application.score = score

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

        return application
