from app-api.core.models import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Unicode(100))
    last_name = db.Column(db.Unicode(100))
    auth_sub = db.Column(db.String(100))
    notifications_enabled = db.Column(db.Boolean())
    notifications_radius_meters = db.Column(db.Float())
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    avatar = db.Column(db.String(100))
    expires_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
