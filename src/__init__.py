from flask import Flask
from config import Config

from src.extensions import db, migrate, bcrypt, login_manager

# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

# from src.models import db
# from flask_migrate import Migrate

# migrate = Migrate()
# bcrypt = Bcrypt()
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicialización de extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)

    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Registro de Blueprints...
    from src.main import bp as main_bp
    from src.auth import bp as auth_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from src.auth import utils

    @app.route('/health')
    def health_check():
        return {
            "status": "up",
            "environment": app.config.get("ENVIRONMENT")
        },200

    return app
