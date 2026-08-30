from src.models import User
from src.extensions import db


def test_register_page(client):
    response = client.get("/auth/register")

    assert response.status_code == 200


def test_register_user(client):
    response = client.post(
        "/auth/register",
        data={
            "username": "usuario_test",
            "email": "usuario@test.com",
            "password": "Password123!",
            "confirm_password": "Password123!"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Ya puedes iniciar sesi" in response.data


def test_login_user(client):
    client.post(
            "/auth/register",
            data={
                "username": "usuario_test",
                "email": "usuario@test.com",
                "password": "Password123!",
                "confirm_password": "Password123!"
            },
            follow_redirects=True
        )

    response = client.post(
        "/auth/login",
        data={
            "email": "usuario@test.com",
            "password": "Password123!"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"dashboard" in response.data.lower()


def test_login_invalid_password(client):
    client.post(
            "/auth/register",
            data={
                "username": "usuario_test",
                "email": "usuario@test.com",
                "password": "Password123!",
                "confirm_password": "Password123!"
            },
            follow_redirects=True
        )

    response = client.post(
        "/auth/login",
        data={
            "email": "usuario@test.com",
            "password": "WrongPass123!"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"dashboard" not in response.data.lower()


def create_test_user(app):
    user = User(
        username="auth test",
        email="auth@test.com"
    )

    user.set_password("Password123!")

    db.session.add(user)
    db.session.commit()

    return user


def test_authenticated_user_can_access_dashboard(client, app):

    create_test_user(app)

    client.post(
        "/auth/login",
        data={
            "email": "auth@test.com",
            "password": "Password123!"
        }
    )

    response = client.get("/auth/dashboard")

    assert response.status_code == 200


def test_logout(client, app):
    create_test_user(app)
    
    client.post(
        "/auth/login",
        data={
            "email": "auth@test.com",
            "password": "Password123!"
        }
    )

    response = client.get(
        "/auth/logout",
        follow_redirects=True
    )

    assert response.status_code == 200


def test_logout_protects_dashboard(client, app):
    create_test_user(app)
        
    client.post(
        "/auth/login",
        data={
            "email": "auth@test.com",
            "password": "Password123!"
        }
    )

    client.get("/auth/logout")

    response = client.get("/auth/dashboard")

    assert response.status_code == 302
    assert "/auth/login" in response.location

