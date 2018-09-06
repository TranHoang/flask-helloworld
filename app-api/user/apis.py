from flask import Blueprint

user_api = Blueprint('user_api', __name__)

@user_api.route("/")
def hello():
    return "Hello World from user api!"