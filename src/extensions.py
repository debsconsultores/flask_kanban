from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from celery import Celery

# Extensión para trabajar con SQLAlchemy
db = SQLAlchemy()

# Extensión para administrar las migraciones de la base de datos
migrate = Migrate()

# Extensión para generar y verificar hashes de contraseñas
bcrypt = Bcrypt()

# Extensión para administrar la autenticación y las sesiones
# de los usuarios
login_manager = LoginManager()

# Vista a la que Flask-Login enviará al usuario
# cuando intente acceder a una ruta protegida
# sin haber iniciado sesión.
#
# IMPORTANTE:
# El endpoint auth.login existirá más adelante,
# cuando creemos el Blueprint de autenticación.
login_manager.login_view = 'auth.login'


# Categoría que utilizarán los mensajes de Flask-Login
# cuando redirija a un usuario no autenticado.
login_manager.login_message_category = 'info'

jwt = JWTManager()

# Instancia de Celery
celery = Celery(__name__)