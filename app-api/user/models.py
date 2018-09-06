from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column
from sqlalchemy.types import (
    Unicode,
    String,
    Boolean,
    Float,
    DateTime,
)

db = SQLAlchemy()

class User(db.Model):
    first_name = Column(Unicode(100))
    last_name = Column(Unicode(100))
    auth_sub = Column(String(100))
    notifications_enabled = Column(Boolean())
    notifications_radius_meters = Column(Float)
    phone = Column(String(100))
    email = Column(String(100))
    avatar = Column(String(100))
    expires_at = Column(DateTime())
    created_at = Column(DateTime())
    updated_at = Column(DateTCreate to ime())
