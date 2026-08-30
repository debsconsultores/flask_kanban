import os
from dotenv import load_dotenv


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-muy-secreta'
    ENVIRONMENT = os.environ.get("FLASK_ENV","production") 

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://flask_user:flask_password@localhost:5432/kanban_dev'

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

