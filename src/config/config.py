import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DB_USER = os.getenv('DB_USER')
    DB_HOSTNAME = os.getenv('DB_HOSTNAME')
    DB_PORT = os.getenv('DB_PORT', 5432)
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_SCOPES = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]
    GOOGLE_USER_INFO_PATH = '/oauth2/v2/userinfo'
    DOMAIN = 'hackdavis.io'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD,
                                                                   DB_HOSTNAME, DB_PORT, DB_NAME)
    USE_SESSION_FOR_NEXT = 1
