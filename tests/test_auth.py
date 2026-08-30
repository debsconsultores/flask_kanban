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

