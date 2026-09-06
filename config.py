import os
from dotenv import load_dotenv


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-muy-secreta'
    ENVIRONMENT = os.environ.get("FLASK_ENV", "production") 

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://flask_user:flask_password@localhost:5432/kanban_dev'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or \
            'dev-jwt-key-muy-secreta-2026-1234567890'

    # Broker utilizado por Celery.
    CELERY_BROKER_URL = os.environ.get(
        "CELERY_BROKER_URL"
    ) or "redis://localhost:6379/0"

    # Backend utilizado para almacenar resultados.
    CELERY_RESULT_BACKEND = os.environ.get(
        "CELERY_RESULT_BACKEND"
    ) or "redis://localhost:6379/0"


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

