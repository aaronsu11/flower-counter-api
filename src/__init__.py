from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pyrebase
from flask_mail import Mail
from .config import Config

firebase = pyrebase.initialize_app(Config.firebase_config)
storage = firebase.storage()
db = SQLAlchemy()
cors = CORS()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    cors.init_app(app)
    mail.init_app(app)

    from .processing_worker import api

    app.register_blueprint(api)

    return app
