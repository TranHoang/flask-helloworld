from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from .models import db
from .create_app import create_app

app = create_app(__name__)

# Configuration
# Create API
api = Api(app)

# Sync up database
db.app = app
db.init_app(app)

bcrypt = Bcrypt()
bcrypt.init_app(app)

# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)

migrate = Migrate(app, db) # this
