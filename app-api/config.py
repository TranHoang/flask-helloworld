import os
from datetime import timedelta

postgres_uri = 'postgresql://postgres:123456@localhost/api'

class BaseConfig():
    """
    Base application configuration
    """
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'invisible_key')
    JWT_SECRET_KEY = 'super-secret'
    # Config JWT expires time in minutes
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 120))


class DevelopmentConfig(BaseConfig):
    """
    Configuration for development env
    """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', "sqlite:///db.sqlite3")


class ProductionConfig(BaseConfig):
    """
    Configuration for production env
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', postgres_uri)
