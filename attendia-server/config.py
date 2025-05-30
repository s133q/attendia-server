import os

SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///attendia.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
