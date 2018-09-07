import os

from flask import Flask
from flask_migrate import Migrate

from core import db
from .user import user_api

app = Flask(__name__)

# Load configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app-api.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# Sync up database
db.app = app
db.init_app(app)

migrate = Migrate(app, db) # this

app.register_blueprint(user_api, url_prefix='/users')

if __name__ == '__main__':
    app.run()
