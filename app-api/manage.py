import os

from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate


from core import db, bcrypt
from user import UserResource, UserListResource
from todo import ToDoResource

app = Flask(__name__)

# Load configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app-api.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# Create API
api = Api(app)

# Sync up database
db.app = app
db.init_app(app)

bcrypt.init_app(app)

migrate = Migrate(app, db) # this

##
## Setup the Api resource routing here
##
api.add_resource(UserResource, '/user/<user_id>')
api.add_resource(UserListResource, '/users')
api.add_resource(ToDoResource, '/todo/<id>')

if __name__ == '__main__':
    app.run()
