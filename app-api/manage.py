import os

from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from core import db, bcrypt
from user import UserResource, UserListResource
from auth.apis import AuthenticationResource
from todo import TodoResource, TodoListResource, CompletedTodoListResource, UnCompletedTodoListResource

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

# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)

migrate = Migrate(app, db) # this

##
## Setup the Api resource routing here
##
api.add_resource(AuthenticationResource, '/auth')
api.add_resource(UserResource, '/user/<user_id>')
api.add_resource(UserListResource, '/users')
api.add_resource(TodoResource, '/todo/<id>')
api.add_resource(TodoListResource, '/todos')
api.add_resource(CompletedTodoListResource, '/todos/completed')
api.add_resource(UnCompletedTodoListResource, '/todos/uncompleted')


if __name__ == '__main__':
    app.run()
