def test_home(client):
    response = client.get("/")

    assert response.status_code == 200


def test_home_page_returns_html(client):
    response = client.get("/")

    assert response.data

    assert response.content_type.startswith("text/html")
