from flask import Flask
from config import Config
from flask_bcrypt import Bcrypt

from src.models import db
from flask_migrate import Migrate

migrate = Migrate()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicialización de extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)

    bcrypt.init_app(app)

    # Registro de Blueprints...
    from src.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    @app.route('/health')
    def health_check():
        return {
            "status": "up",
            "environment": app.config.get("ENVIRONMENT")
        },200

    return app
