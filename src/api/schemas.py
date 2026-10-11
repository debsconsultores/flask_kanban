from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields
from src.extensions import db

from src.models import Task


class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True
        # sqla_session = db.session


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class TaskCreateSchema(Schema):
    title = fields.String(required=True)
    content = fields.String(required=False, allow_none=True)


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
login_schema = LoginSchema()
task_create_schema = TaskCreateSchema()