import os
from dotenv import load_dotenv


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-muy-secreta'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    