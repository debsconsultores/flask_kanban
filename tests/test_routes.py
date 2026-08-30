def test_home_page(client):
    # Realizamos una petición GET a la página principal.
    response = client.get("/")

    # La página debe responder correctamente.
    assert response.status_code == 200


def test_page_not_found(client):
    # Realizamos una petición GET a una ruta inexistente
    response = client.get("/ruta-indexistente")

    # La página debe responder correctamente.
    assert response.status_code == 404


def test_dashboard_requires_login(client):
    response = client.get("/auth/dashboard")

    assert response.status_code == 302

    assert "/login" in response.location
