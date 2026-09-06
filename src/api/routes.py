from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
    )
from sqlalchemy import select

from src.api import bp
from src.api.schemas import tasks_schema, task_schema
from src.extensions import db
from src.models import Task, User

from src.tasks import saludar

@bp.route("/test", methods=["GET"])
def test_api():
    return jsonify({
        "mensaje": "API funcionando satisfactoriamente"
    }), 200




@bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    # tasks = Task.query.all()
    user_id = get_jwt_identity()

    statement = select(Task).where(
        Task.user_id == int(user_id),
        Task.delete_at.is_(None)
        
    )

    tasks = db.session.execute(statement).scalars().all()

    result = tasks_schema.dump(tasks)

    return jsonify(result), 200



@bp.route('/login', methods=["POST"])
def api_login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = db.session.scalar(
        select(User).where(User.email == email)
    )

    if not user or not user.check_password(password):
        return jsonify({
            "error" : "Credenciales inválidas"
        }),401

    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "access_token": access_token
    }),200


@bp.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    # Obtenemos la identidad del usuario autenticado.
    user_id = get_jwt_identity()

    # Obtenemos los datos enviados en formato JSON.
    data = request.get_json()

    # Validamos que exista información en la petición.
    if not data:
        return error_response("No se recibieron datos", 400)

    # Obtenemos los campos de la nueva tarea.
    title = data.get("title")
    content = data.get("content")

    # Validamos el título.
    if not title:
        return error_response("El título es obligatorio", 400)

    # Creamos la tarea asociándola al usuario autenticado.
    task = Task(
        title=title,
        content=content,
        user_id=int(user_id)
    )

    # Guardamos la nueva tarea.
    db.session.add(task)
    db.session.commit()

    # Convertimos la tarea a JSON.
    result = task_schema.dump(task)

    # Devolvemos la tarea creada.
    return jsonify(result), 201


@bp.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    # Obtenemos la identidad del usuario autenticado.
    user_id = get_jwt_identity()

    # Obtenemos los datos enviados por el cliente.
    data = request.get_json()

    # Buscamos únicamente una tarea perteneciente
    # al usuario autenticado.
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == int(user_id)
    )

    task = db.session.execute(
        statement
    ).scalar_one_or_none()

    # Si la tarea no existe o no pertenece al usuario,
    # devolvemos un error 404.
    if task is None:
        return error_response("Tarea No Encontrada", 404)

    # Actualizamos los campos recibidos.
    if "title" in data:
        if not data["title"].strip():
            return error_response("El título no puede estar vacío", 400)

        task.title = data["title"]

    if "content" in data:
        if not data["content"].strip():
            return error_response("El contenido no puede estar vacío", 400)

        if not isinstance(data["content"], str):
            return error_response("El contenido debe ser una cadena", 400)

        task.content = data["content"]

    # Guardamos los cambios.
    db.session.commit()

    # Serializamos la tarea actualizada.
    result = task_schema.dump(task)

    return jsonify(result), 200


@bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    # Obtenemos la identidad del usuario autenticado.
    user_id = get_jwt_identity()

    # Buscamos la tarea perteneciente al usuario autenticado.
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == int(user_id)
    )

    task = db.session.execute(
        statement
    ).scalar_one_or_none()

    # Si no existe o no pertenece al usuario,
    # no permitimos realizar la operación.
    if task is None:
        return error_response("Tarea no encontrada", 404)

    # Realizamos el borrado lógico.
    task.delete()

    return jsonify({
        "message": "Tarea eliminada correctamente"
    }), 200


def error_response(message, status_code):
    return jsonify({
        "error": message
    }), status_code


@bp.route("/test-celery", methods=["GET"])
def test_celery():

    # Enviamos la tarea al broker.
    task = saludar.delay("Daniel")

    return {
        "message": "Tarea enviada correctamente",
        "task_id": task.id
    }, 202