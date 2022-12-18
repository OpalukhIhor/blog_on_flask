from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_msearch import Search
from flask_sqlalchemy import SQLAlchemy

from config import Config


# Variables
db = SQLAlchemy()
migrate = Migrate()

login = LoginManager()
login.login_view = 'user.login'
login.login_message = 'Please log in to access this page.'

mail = Mail()

search = Search()


# Application Factory
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    login.init_app(app)

    mail.init_app(app)

    search.init_app(app)


#  Register Blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.user import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/user')

    from app.post import bp as post_bp
    app.register_blueprint(post_bp)

    from app.errors import bp as error_bp
    app.register_blueprint(error_bp)

    return app
