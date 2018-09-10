from user.models import User


def authenticate(email, password):
    """
    Check username and password
    """
    user = User.query.get_by_email(email)
    if user and user.check_password(password):
        return user


def identity(payload):
    """
    Get user information from payload.
    This payload is decoded by flask-jwt module.
    """
    user_id = payload['identity']
    return User.query.get_by_id(user_id)
