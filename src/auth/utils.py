from src.extensions import login_manager
from src.models import User
from src.extensions import db


@login_manager.user_loader
def load_user(user_id):
    # Esta función le dice a Flask Login cómo obtener un usuario por Id
    # return User.query.get(int(user_id))
    return db.session.get(User, int(user_id))