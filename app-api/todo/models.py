from flask_sqlalchemy import BaseQuery

from core.models import (
    db,
    TimestampMixin
)

#################################################
# Todo model and query set
#################################################

class TodoQuery(BaseQuery):
    def get_by_id(self, id):
        return self.get(ident=id)

class Todo(db.Model, TimestampMixin):
    query_class = TodoQuery

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False)
    title = db.Column(db.Unicode(100))
    due_date = db.Column(db.DateTime())
    completed = db.Column(db.Boolean())
    completed_date = db.Column(db.DateTime())
