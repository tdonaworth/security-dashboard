import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    # SERVER SETTINGS
    PORT = 5050
    # DB SETTINGS
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///" + os.path.join(
        basedir, "app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.getenv("REDIS_URL") or "redis://"
    # SECRET FOR CSRF TOKEN
    SECRET_KEY = os.getenv("CSRF_KEY")

    # S MTP MAIL SETTINGS
    SMTP_SERVER = os.getenv("SMTP_SERVER")  # Set to None to disable email error logs
    SMTP_PORT = os.getenv("SMTP_PORT") or 587  # 25 for insecure port
    SMTP_USE_TLS = os.getenv("SMTP_USE_TLS") is not None
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    ADMINS = os.getenv("ADMIN_EMAIL")

    # API TOKENS (DEV)
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
