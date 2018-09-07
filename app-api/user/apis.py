from flask import Blueprint
from .models import User

user_api = Blueprint('user_api', __name__)

@user_api.route("/")
def hello():
    return "Hello World from user api!"