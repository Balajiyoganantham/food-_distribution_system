from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
bcrypt = Bcrypt()

login_manager.login_view = 'main.login'
login_manager.login_message_category = "info"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app
