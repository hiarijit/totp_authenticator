import os
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "default-unsafe-secret"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False