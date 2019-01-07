import csv
import time
from datetime import datetime, timedelta, date
from collections import defaultdict
from sqlalchemy.sql.expression import func

from src.shared import Shared
from src.models.Answer import Answer
from src.models.User import User
from src.models.Question import Question
from src.models.schema.Application import Application
from src.models.Settings import Settings
from src.models.enums.QuestionType import QuestionType
from src.models.lib.ModelUtils import ModelUtils

db = Shared.db


class ApplicationQueries():
    @staticmethod
    def insert(csv_file, question_rows, session):
        """Insert new rows extracted from csv_file"""
        start = time.perf_counter()

        applications = ApplicationQueries.get_applications_from_csv(csv_file)
        rows = ApplicationQueries.convert_applications_to_rows(applications)

        object_load = time.perf_counter()

        print("Applcations load time", object_load - start)

        session.bulk_save_objects(rows, return_defaults=True)

        applications_save = time.perf_counter()

        print("Applications save time", applications_save - object_load)

        Answer.insert(question_rows, applications, rows, session)
        return rows

    @staticmethod
    def insert_without_duplicates(csv_file, question_rows):
        """Insert new rows extracted from csv_file"""
        start = time.perf_counter()

        Question.get_questions_from_csv(csv_file) #need to advance the csv_file reader
        question_types = Question.get_question_types_from_csv(csv_file)
        applications = ApplicationQueries.get_applications_from_csv(csv_file)

        email_index = 0
        for i in range(len(question_types)):
            try:
                qt = QuestionType[question_types[i]]
                if qt == QuestionType.email:
                    email_index = i
                    break
            except KeyError:
                raise ValueError(
                    'question type {question_type} not recognized'.format(
                        question_type=question_types[i]))

        object_load = time.perf_counter()

        print("Applcations load time", object_load - start)

        rows = []

        for application in applications:
            if not Answer.check_duplicate_email(application[email_index]):
                application_row = ApplicationQueries.convert_application_to_row(application)

                db.session.add(application_row)

                rows.append(application_row)
                Answer.insert_ORM(question_rows, [application], [application_row])

        applications_save = time.perf_counter()

        print("Applications save time", applications_save - object_load)

        return rows

    @staticmethod
    def get_applications_from_csv(csv_file):
        """Get applications from CSV file"""
        applications = list(csv.reader(csv_file))
        return applications[1:]

    @staticmethod
    def convert_applications_to_rows(applications):
        """Convert applications into rows to insert into database"""
        return [ApplicationQueries.convert_application_to_row(application) for application in applications]

    @staticmethod
    def convert_application_to_row(application):
        """Convert application into row to insert into database"""
        return Application(score=0, date_added=date.today())

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
        application = ApplicationQueries.get_currently_assigned_application_for_user(user_id)
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
            .filter(Application.id == application_id).first()

    @staticmethod
    def get_all_applications_for_user(user_id):
        """Returns all applications associated with user ID"""
        cutoff = datetime.now() - timedelta(hours=1)
        return db.session.query(Application) \
            .filter(Application.assigned_to == user_id) \
            .filter((Application.score != 0) | ((Application.score == 0) & (Application.last_modified > cutoff)))

    @staticmethod
    def get_count_of_applications_for_user(user_id):
        """Returns count of applications associated with user ID"""
        cutoff = datetime.now() - timedelta(hours=1)
        return db.session.query(func.count(Application.id)) \
            .filter(Application.assigned_to == user_id) \
            .filter((Application.score != 0) | ((Application.score == 0) & (Application.last_modified > cutoff))) \
            .scalar()

    @staticmethod
    def count_applications():
        """Counts number of applications in database"""
        return db.session.query(func.count(Application.id)).scalar()

    @staticmethod
    def count_accepted():
        """Counts number of applications in database"""
        accepted = ApplicationQueries.get_accepted_ids_query()
        return db.session.query(Application).join(accepted, accepted.c.id == Application.id).count()

    @staticmethod
    def get_all_applications():
        """Returns all applications"""
        return db.session.query(Application)

    @staticmethod
    def skip_application(user_id):
        """Returns next application for user to review"""
        application = ApplicationQueries.get_currently_assigned_application_for_user(user_id)

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
    def update_score_and_feedback(application, score, feedback, locked_by):
        """Updates the score for an application"""
        application.score = score
        application.feedback = feedback

        if application.assigned_to != locked_by:
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
        return db.session.query(func.avg(Application.score), func.stddev(Application.score), User.id) \
            .filter(Application.score != 0) \
            .join(User, (User.id == Application.locked_by) | (User.id == Application.assigned_to)) \
            .group_by(User.id) \
            .all()

    @staticmethod
    def standardize_scores():
        """Updates the standardized scores for all applications"""
        stats_per_user = ApplicationQueries.get_mean_stddev_scores_per_user()
        scored_applications = ApplicationQueries.get_scored_applications()

        scored_applications_per_user = defaultdict(list)

        for application in scored_applications:
            user = application.assigned_to
            if application.locked_by is not None:
                user = application.locked_by

            scored_applications_per_user[user].append(application)

        for (user, stats) in zip(sorted(scored_applications_per_user), stats_per_user):
            stddev = stats[1]
            if stddev == 0 or stddev is None:
                stddev = 1
            for application in scored_applications_per_user[user]:
                ApplicationQueries.set_standardized_score(application, (application.score - stats[0]) / stddev)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def question_answer_matrix_subquery():
        return db.session.query(Application.id, func.sum(Answer.answer_weight * Question.weight).label("sum_values")) \
        .join(Answer) \
        .join(Question) \
        .group_by(Application.id).subquery()

    @staticmethod
    def rank_participants():
        ApplicationQueries.standardize_scores()

        firstNames = db.session.query(Application.id) \
        .join(Answer) \
        .join(Question) \
        .filter(Question.question_type == QuestionType.firstName) \
        .add_column(Answer.answer) \
        .subquery()

        lastNames = db.session.query(Application.id) \
        .join(Answer) \
        .join(Question) \
        .filter(Question.question_type == QuestionType.lastName) \
        .add_column(Answer.answer) \
        .subquery()

        emails = db.session.query(Application.id) \
        .join(Answer) \
        .join(Question) \
        .filter(Question.question_type == QuestionType.email) \
        .add_column(Answer.answer) \
        .subquery()

        answer_values = ApplicationQueries.question_answer_matrix_subquery()

        results = db.session.query(Application.id, firstNames.c.answer, lastNames.c.answer, emails.c.answer, func.sum(answer_values.c.sum_values + Application.standardized_score)) \
        .filter(Application.score != 0) \
        .join(answer_values, answer_values.c.id == Application.id) \
        .join(firstNames, firstNames.c.id == Application.id) \
        .join(lastNames, lastNames.c.id == Application.id) \
        .join(emails, emails.c.id == Application.id) \
        .group_by(Application.id, firstNames.c.answer, lastNames.c.answer, emails.c.answer) \
        .order_by(func.sum(answer_values.c.sum_values + Application.standardized_score).desc().nullslast()) \
        .all()

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

        return results

    @staticmethod
    def get_accepted_ids_query():
        limit = Settings.get_settings().accept_limit

        ApplicationQueries.standardize_scores()

        answer_values = ApplicationQueries.question_answer_matrix_subquery()

        return db.session.query(Application.id, func.sum(answer_values.c.sum_values + Application.standardized_score)) \
        .filter(Application.score != 0) \
        .group_by(Application.id) \
        .order_by(func.sum(answer_values.c.sum_values + Application.standardized_score).desc().nullslast()) \
        .limit(limit) \
        .subquery()


    @staticmethod
    def count_values_per_answer():
        accepted = ApplicationQueries.get_accepted_ids_query()

        answer_totals_q = db.session.query(func.count(Answer.id), Answer.answer, Question.question, Answer.question_id) \
        .join(Question) \
        .join(accepted) \
        .filter(Question.question_type == QuestionType.demographic) \
        .group_by(Answer.question_id, Question.question, Answer.answer) \
        .order_by(Answer.question_id)
        
        print(answer_totals_q)
        answer_totals = answer_totals_q.all()

        return answer_totals
