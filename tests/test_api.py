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


def test_create_task(client, user):
    """Verifica que un usuario autenticado pueda crear una tarea."""

    token = get_auth_token(client, user)

    response = client.post(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Tarea de prueba",
            "content": "Contenido de la tarea"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["title"] == "Tarea de prueba"
    assert data["content"] == "Contenido de la tarea"


def test_create_and_get_task(client, user):
    """Verifica que una tarea creada aparezca en el listado."""

    token = get_auth_token(client, user)

    create_response = client.post(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Tarea para consultar",
            "content": "Contenido de prueba"
        }
    )

    assert create_response.status_code == 201

    response = client.get(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["title"] == "Tarea para consultar"


def test_update_task(client, user):
    """Verifica que un usuario pueda actualizar una tarea."""

    token = get_auth_token(client, user)

    create_response = client.post(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Título original",
            "content": "Contenido original"
        }
    )

    assert create_response.status_code == 201

    created_task = create_response.get_json()

    task_id = created_task["id"]

    update_response = client.put(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Título actualizado",
            "content": "Contenido actualizado"
        }
    )

    assert update_response.status_code == 200

    data = update_response.get_json()

    assert data["title"] == "Título actualizado"
    assert data["content"] == "Contenido actualizado"


def test_delete_task(client, user):
    """Verifica que una tarea pueda eliminarse mediante Soft Delete."""

    token = get_auth_token(client, user)

    create_response = client.post(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Tarea para eliminar",
            "content": "Esta tarea será eliminada"
        }
    )

    assert create_response.status_code == 201

    created_task = create_response.get_json()

    task_id = created_task["id"]

    delete_response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert delete_response.status_code == 200


def test_delete_task_no_show(client, user):
    """Verifica que una tarea pueda eliminarse mediante Soft Delete."""

    token = get_auth_token(client, user)

    create_response = client.post(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Tarea para eliminar",
            "content": "Esta tarea será eliminada"
        }
    )

    assert create_response.status_code == 201

    created_task = create_response.get_json()

    task_id = created_task["id"]

    delete_response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert delete_response.status_code == 200

    response = client.get(
        "/api/v1/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 0


def test_create_task_requires_authentication(client):
    """Verifica que un usuario no autenticado no pueda crear tareas."""

    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Tarea sin autenticación",
            "content": "No debería crearse"
        }
    )

    assert response.status_code == 401

