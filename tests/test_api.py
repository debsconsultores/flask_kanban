import pytest

from src.extensions import db
from src.models import User


@pytest.fixture
def user(app):

    with app.app_context():

        user = User(
            username="testuser",
            email="test@example.com"
        )

        user.set_password("Password123!")

        db.session.add(user)
        db.session.commit()

        return {
            "email": "test@example.com",
            "password": "Password123!"
        }


def test_api_login(client, user):
    response = client.post(
        "/api/v1/login",
        json={
            "email": "test@example.com",
            "password": "Password123!"
        }
    )


    assert response.status_code ==200

    data = response.get_json()

    assert "access_token" in data


def get_auth_token(client, user):
    response = client.post(
        "/api/v1/login",
        json={
            "email": user["email"],
            "password": user["password"]
        }
    )

    return response.get_json()["access_token"]


def test_get_tasks_requires_authentication(client):
    response = client.get("/api/v1/tasks")

    assert response.status_code == 401


def test_get_tasks_authenticated(client, user):

    token = get_auth_token(client, user)

    response = client.get(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)


def test_api_login_invalid_password(client, user):
    """Verifica que el login rechace una contraseña incorrecta."""

    response = client.post(
        "/api/v1/login",
        json={
            "email": user["email"],
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401


