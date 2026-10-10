from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.extensions import db

from src.models import Task


class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True
        sqla_session = db.session


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)