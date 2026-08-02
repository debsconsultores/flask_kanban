from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    
    @app.route('/health')
    def health_check():
        return {
            "status": "up",
            "environment": app.config.get("ENVIRONMENT")
        },200

    return app