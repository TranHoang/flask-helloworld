from flask import Flask
from .user import user_api

app = Flask(__name__)
app.register_blueprint(user_api, url_prefix='/users')

if __name__ == '__main__':
    app.run()