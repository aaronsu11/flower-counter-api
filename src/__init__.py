from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pyrebase
from flask_mail import Mail
from .config import Config

firebase_config = {
    "apiKey": "AIzaSyBmbEYCRih5N8ls-UYgv26OnAz67IDR8gk",
    "authDomain": "flower-counter.firebaseapp.com",
    "databaseURL": "https://flower-counter.firebaseio.com",
    "projectId": "flower-counter",
    "storageBucket": "flower-counter.appspot.com",
    "messagingSenderId": "276724841166",
    "appId": "1:276724841166:web:9a24d03f468502b5992e9f",
    "measurementId": "G-4HSDYZE7SQ",
}

firebase = pyrebase.initialize_app(firebase_config)

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
