import os

APP_ENV = os.getenv("FLASK_ENV")

if APP_ENV == "test":
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
else:
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
        DB_USER=os.getenv("DB_USER"),
        DB_PASSWORD=os.getenv("DB_PASSWORD"),
        DB_HOST=os.getenv("DB_HOST"),
        DB_PORT=os.getenv("DB_PORT"),
        DB_NAME=os.getenv("DB_NAME"),
    )
    # Connection pool settings for PostgreSQL


class ApplicationConfig:
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL")
