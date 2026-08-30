from flask import jsonify

from src.api import bp
from src.api.schemas import tasks_schema
from src.models import Task

@bp.route("/test", methods=["GET"])
def test_api():
    return jsonify({
        "mensaje": "API funcionando satisfactoriamente"
    }), 200




@bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()

    result = tasks_schema.dump(tasks)

    return jsonify(result), 200