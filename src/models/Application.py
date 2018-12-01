import csv
from datetime import datetime, timedelta
from scipy import stats
from sqlalchemy.sql.expression import func

from src.shared import Shared
from src.models.Answer import Answer
from src.models.lib.ModelUtils import ModelUtils
from src.models.lib.Serializer import Serializer

db = Shared.db


class Application(db.Model, ModelUtils, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    locked_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to_user = db.relationship('User', foreign_keys=assigned_to)
    locked_by_user = db.relationship('User', foreign_keys=locked_by)
    score = db.Column(db.Integer, nullable=False)
    standardized_score = db.Column(db.Float)
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
    def set_standardized_scores(applications):
        """Calculate and set standardize scores for applications"""
        scores = [application.score for application in applications]
        standardized_scores = stats.zscore(scores)
        return list(
            map(lambda application, standardized_score: Application.set_standardized_score(application, standardized_score),
                applications, standardized_scores))

    @staticmethod
    def set_standardized_score(application, standardized_score):
        """Set standardize score for an application"""
        application.standardized_score = standardized_score
        return application

    @staticmethod
    def get_currently_assigned_application_for_user(user_id):
        """Returns assigned application associated with user ID"""
        cutoff = datetime.now() - timedelta(hours=1)
        return db.session.query(Application) \
            .filter(
            (Application.assigned_to == user_id) & (Application.score == 0) & (Application.last_modified > cutoff)) \
            .first()

    @staticmethod
    def get_application_for_user(user_id):
        """Returns application for user to review"""
        application = Application.get_currently_assigned_application_for_user(user_id)
        if application is None:
            cutoff = datetime.now() - timedelta(hours=1)
            application = db.session.query(Application) \
                .filter((Application.score == 0) & (
                    (Application.assigned_to == None) | (Application.last_modified <= cutoff))) \
                .limit(50) \
                .from_self() \
                .order_by(func.random()) \
                .first()

            if application is None:
                return None

            application.assigned_to = user_id

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

        return application

    @staticmethod
    def get_application(application_id):
        """Returns all applications associated with user ID"""
        cutoff = datetime.now() - timedelta(hours=1)
        return db.session.query(Application) \
            .filter(Application.id == application_id).one()


    @staticmethod
    def get_application_id_by_user(application_id, user_id):
        """Returns all applications associated with user ID"""
        return db.session.query(Application) \
            .filter((Application.assigned_to == user_id) & (Application.id == application_id)).one()


    @staticmethod
    def get_all_applications_for_user(user_id):
        """Returns all applications associated with user ID"""
        cutoff = datetime.now() - timedelta(hours=1)
        return db.session.query(Application) \
            .filter((Application.assigned_to == user_id) & ((Application.score != 0) | ((Application.score == 0) & (Application.last_modified > cutoff))))

    @staticmethod
    def get_all_applications():
        """Returns all applications"""
        return db.session.query(Application)

    @staticmethod
    def skip_application(user_id):
        """Returns next application for user to review"""
        application = Application.get_currently_assigned_application_for_user(user_id)

        if application is None:
            return None

        application.assigned_to = None

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

        return application

    @staticmethod
    def update_score(application, score, locked_by):
        """Updates the score for an application"""
        application.score = score
        application.locked_by = locked_by

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_scored_applications():
        """Returns all scored applications"""
        return db.session.query(Application) \
            .filter(Application.score != 0) \
            .all()

    @staticmethod
    def standardize_scores():
        """Updates the standardized scores for all applications"""
        scored_applications = Application.get_scored_applications()

        # gets all unique user ids
        user_ids = {application.assigned_to for application in scored_applications}

        # creates a dict to map between user_id and list of applications scored by that user
        user_to_applications = {
            user_id: list(
                filter(lambda application: application.assigned_to == user_id, scored_applications))
            for user_id in user_ids
        }

        # creates a dict to map between user_id and list of applications scored by that user with standardized_scores set
        user_to_applications_with_standardized_scores = {
            user_id: Application.set_standardized_scores(applications)
            for user_id, applications in user_to_applications.items()
        }

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
