import argparse
import sys

from flask_sqlalchemy import SQLAlchemy

from app import app
from src.models.enums.Role import Role

db = SQLAlchemy()

from src.models.Action import Action
from src.models.Answer import Answer
from src.models.Application import Application
from src.models.OAuth import OAuth
from src.models.Question import Question
from src.models.User import User

db.init_app(app)


def successful_exit(message):
    """prints a message and exits"""
    print(message)
    exit(0)


def exit_with_error(error_message):
    """prints an error to stderr and exits"""
    print(error_message, file=sys.stderr)
    exit(1)


def get_user_email(email):
    """Returns user associated with user Email"""
    return db.session.query(User) \
        .filter(User.email == email) \
        .first()


def make_admin():
    """Makes a user an admin"""
    print('What is the email of the user you are making an admin')
    email_str = input()

    user = get_user_email(email_str)
    if user is None:
        exit_with_error('User does not exist. Exiting.')

    user.role = Role.admin

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        exit_with_error('Error occurred while persisting: {e}. Exiting.')

    successful_exit(f"Made user {email_str} an admin.")


def remove_admin():
    """Removes a user as an admin"""
    print('What is the email of the user you are removing as an admin')
    email_str = input()

    user = get_user_email(email_str)
    if user is None:
        exit_with_error('User does not exist. Exiting.')

    user.role = Role.user

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        exit_with_error('Error occurred while persisting: {e}. Exiting.')

    successful_exit(f"Removed user {email_str} as an admin.")


def drop_database():
    """Drop the database"""
    print(
        'Are you absolutely sure you want to proceed with dropping the database? This action is irreversible. [YES or NO]'
    )
    confirmation = input()
    if confirmation != 'YES':
        exit('Confirmation not received. Exiting.')

    try:
        Action.__table__.drop(db.engine)
        OAuth.__table__.drop(db.engine)
        Answer.__table__.drop(db.engine)
        Application.__table__.drop(db.engine)
        Question.__table__.drop(db.engine)
        User.__table__.drop(db.engine)
    except Exception as e:
        exit_with_error(f"Error occurred while dropping database: {e}. Exiting.")

    successful_exit('Dropped database.')


commands = {
    'make-admin': make_admin,
    'remove-admin': remove_admin,
    'drop-database': drop_database,
}

parser = argparse.ArgumentParser(description='Administrate the Flask app')
parser.add_argument(
    '-c', '--command', default='make-admin', choices=list(commands.keys()),
    type=str)  # optional, default is 'make-admin'

if __name__ == '__main__':
    args = parser.parse_args()
    command = args.command

    # check if command is a valid option
    if command not in commands:
        exit_with_error(f"command {command} is not valid. Exiting.")

    func = commands[command]

    with app.app_context():
        func()
