import pytest
from src import create_app
from src.extensions import db
from config import TestConfig


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():

        db.create_all()

        yield app

        db.drop_all()

    # return app


@pytest.fixture
def client(app):
    return app.test_client()