import pytest
from src import create_app
from src.extensions import db
from config import TestConfig
from src.models import User


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


@pytest.fixture
def user(app):
    user = User(
        username="auth test",
        email="auth@test.com"
    )

    user.set_password("Password123!")

    db.session.add(user)
    db.session.commit()

    return user