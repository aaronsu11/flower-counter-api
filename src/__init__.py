from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pyrebase
from flask_mail import Mail
import os

db_user = os.environ.get("CLOUD_SQL_USERNAME")
db_pass = os.environ.get("CLOUD_SQL_PASSWORD")
db_name = os.environ.get("CLOUD_SQL_DATABASE_NAME")
cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")
host = "/cloudsql/{}".format(cloud_sql_connection_name)

firebase_config = {
    "apiKey": "AIzaSyBE-xgkJMD5o1hgU_C_dx82lfMFW7HKQe0",
    "authDomain": "affable-tangent-247104.firebaseapp.com",
    "databaseURL": "https://affable-tangent-247104.firebaseio.com",
    "projectId": "affable-tangent-247104",
    "storageBucket": "affable-tangent-247104.appspot.com",
    "messagingSenderId": "44158393615",
    "appId": "1:44158393615:web:4328365a2657e8f6",
}

firebase = pyrebase.initialize_app(firebase_config)

storage = firebase.storage()

mail_settings = {
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    # "MAIL_USERNAME": os.environ["EMAIL_USER"],
    # "MAIL_PASSWORD": os.environ["EMAIL_PASSWORD"],
    "MAIL_USERNAME": "ssd951106@gmail.com",
    "MAIL_PASSWORD": "19951106ssd",
    "MAIL_DEFAULT_SENDER": ("SRV team", "ssd951106@gmail.com"),
    "MAIL_MAX_EMAILS": 3
    # "MAIL_ASCII_ATTACHMENTS": False
}

db = SQLAlchemy()
cors = CORS()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.update(mail_settings)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
        user=db_user, pw=db_pass, url=host, db=db_name
    )

    db.init_app(app)
    cors.init_app(app)
    mail.init_app(app)

    from .processing_worker import api

    app.register_blueprint(api)

    return app
