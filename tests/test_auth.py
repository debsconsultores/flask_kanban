def test_register_page(client):
    response = client.get("/auth/register")

    assert response.status_code == 200


def test_register_user(client):
    response = client.post(
        "/auth/register",
        data={
            "username":"usuario_test",
            "email":"usuario@test.com",
            "password":"Password123!"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Ya puedes iniciar sesi" in response.data


