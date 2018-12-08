import csv
import time
from datetime import datetime, timedelta
from collections import defaultdict
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import aliased

from src.shared import Shared
from src.models.Answer import Answer
from src.models.User import User
from src.models.Question import Question
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
    def insert(csv_file, question_rows, session):
        """Insert new rows extracted from csv_file"""
        start = time.perf_counter()

        applications = Application.get_applications_from_csv(csv_file)
        rows = Application.convert_applications_to_rows(applications)

        object_load = time.perf_counter()

        print("Applcations load time", object_load - start)

        session.bulk_save_objects(rows, return_defaults=True)

        applications_save = time.perf_counter()

        print("Applications save time", applications_save - object_load)

        Answer.insert(question_rows, applications, rows, session)
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
        """Returns an application, for admin or server-side"""
        return db.session.query(Application) \
            .filter(Application.id == application_id).one()


    @staticmethod
    def get_application_id_by_user(application_id, user_id):
        """Returns all an application associated with user ID"""
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
    def get_mean_stddev_scores_per_user():
        """Returns all scored applications"""
        return db.session.query(Application) \
            .filter(Application.score != 0) \
            .join(User, (User.id == Application.locked_by) | (User.id == Application.assigned_to)) \
            .from_self(func.avg(Application.score), func.stddev(Application.score), User.id) \
            .group_by(User.id) \
            .all()

    @staticmethod
    def standardize_scores():
        """Updates the standardized scores for all applications"""
        stats_per_user = Application.get_mean_stddev_scores_per_user()
        scored_applications = Application.get_scored_applications()

        scored_applications_per_user = defaultdict(list)

        for application in scored_applications:
            user = application.assigned_to
            if application.locked_by is not None:
                user = application.locked_by

            scored_applications_per_user[user].append(application)

        for (user, stats) in zip(sorted(scored_applications_per_user), stats_per_user):
            for application in scored_applications_per_user[user]:
                Application.set_standardized_score(application, (application.score - stats[0]) / stats[1])

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def rank_participants():
        Application.standardize_scores()

        answer_values = db.session.query(Application.id, func.sum(Answer.answer_weight * Question.weight)) \
        .join(Answer) \
        .join(Question) \
        .group_by(Application.id) \
        .all()
