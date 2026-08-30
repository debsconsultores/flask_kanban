from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
    )
from sqlalchemy import select

from src.api import bp
from src.api.schemas import tasks_schema
from src.extensions import db
from src.models import Task, User

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
        Task.user_id == int(user_id)
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


