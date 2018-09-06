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

class Offering(db.Model):
    title = Column(Unicode(100))
    description = Column(Unicode(255))
    google_place_id = Column(Unicode(100))
    address = Column(Unicode(255))
    geo: {
      type: [Number, Number],
      index: '2d'
    },
    image: String,
    user_id: {type: mongoose.Schema.Types.ObjectId, ref: 'User' },
    expires_at: Date,
  },
  {
    timestamps: {
      createdAt: 'created_at',
      updatedAt: 'updated_at',
    },