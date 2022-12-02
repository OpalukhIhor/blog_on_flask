from flask import Flask, current_app

from config import Config

# Application Factory
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

#  Registr Blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
