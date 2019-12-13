import os


class Config:

    # Firebase config
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

    # Cloud SQL config
    db_user = os.environ.get("CLOUD_SQL_USERNAME")
    db_pass = os.environ.get("CLOUD_SQL_PASSWORD")
    db_name = os.environ.get("CLOUD_SQL_DATABASE_NAME")
    cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")
    # host = "/cloudsql/{}".format(cloud_sql_connection_name)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQL connection (choose one)
    if cloud_sql_connection_name:
        # a. Cloud SQL config
        SQLALCHEMY_DATABASE_URI = "postgresql+pg8000://{user}:{pw}@/{db}?unix_sock=/cloudsql/{instance}/.s.PGSQL.5432".format(
            user=db_user, pw=db_pass, db=db_name, instance=cloud_sql_connection_name
        )
    elif False:
        # b. Heroku config
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    else:
        # c. Local config
        SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

    # Gmail config
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # MAIL_USERNAME = os.environ["EMAIL_USER"]
    # MAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
    MAIL_USERNAME = "vyepproject@gmail.com"
    MAIL_PASSWORD = "clare50orange"
    MAIL_DEFAULT_SENDER = ("UNSW FCS", "vyepproject@gmail.com")
    MAIL_MAX_EMAILS = 3
    # MAIL_ASCII_ATTACHMENTS = False
