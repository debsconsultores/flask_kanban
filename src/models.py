from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


db = SQLAlchemy()


class SoftDeleteMixin:
    delete_at = db.Column(db.DateTime, nullable=True)

    def delete(self):
        self.delete_at = datetime.now(timezone.utc)
        db.session.add(self)
        db.session.commit()

    def restore(self):
        self.delete_at = None
        db.session.add(self)
        db.session.commit()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='author', lazy=True)


class Task(db.Model, SoftDeleteMixin):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    