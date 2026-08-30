from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.models import Task


class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)