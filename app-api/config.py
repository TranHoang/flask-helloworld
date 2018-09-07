import os
postgres_uri = 'postgresql://postgres:123456@localhost/api'

class BaseConfig():
    """
    Base application configuration
    """
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'invisible_key')


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', "sqlite:///db.sqlite3")


class ProductionConfig(BaseConfig):
    """
    Production configuration
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', postgres_uri)
