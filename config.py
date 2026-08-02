import os
from dotenv import load_dotenv


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-muy-secreta'
    ENVIRONMENT = os.environ.get("FLASK_ENV","production") 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
