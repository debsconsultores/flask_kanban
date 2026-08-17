from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_login import UserMixin
# from src import login_manager

# db = SQLAlchemy()
from src.extensions import db, login_manager


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


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='author', lazy=True)
    password_hash = db.Column(db.String(128))


class Task(db.Model, SoftDeleteMixin):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    # Esta función le dice a Flask Login cómo obtener un usuario por Id
    # return User.query.get(int(user_id))
    return db.session.get(User, int(user_id))

