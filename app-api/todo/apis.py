from datetime import datetime
from flask_restful import(
    Resource,
    reqparse,
    marshal,
    marshal_with,
    fields)
from flask_jwt_extended import get_jwt_identity, jwt_required
from core.utils import date_time_parsing, SerializeDateTime
from .models import Todo

resource_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'title': fields.String,
    'due_date': SerializeDateTime(attribute='due_date'),
    'completed': fields.Boolean,
    'completed_date': SerializeDateTime(attribute='completed_date'),
}

#################################################################
# TodoResource
# lets you GET/DELETE or UPDATE a Todo item
#################################################################

todo_parser = reqparse.RequestParser()
todo_parser.add_argument('title', type=str)
todo_parser.add_argument('due_date', type=date_time_parsing)
todo_parser.add_argument('completed', type=bool)


class TodoResource(Resource):

    @jwt_required
    @marshal_with(resource_fields)
    def get(self, id):
        user_id = get_jwt_identity()
        todo = Todo.query \
            .by_owner_and_id(user_id, id) \
            .first()
        return todo

    @jwt_required
    @marshal_with(resource_fields)
    def put(self, id):
        """
        Update an Todo item
        """
        data = todo_parser.parse_args()
        user_id = get_jwt_identity()
        todo = Todo.query \
            .by_owner_and_id(user_id, id) \
            .first()

        todo.update(data)
        return todo


#################################################################
# TodoListResource
# lets you POST to create a Todo item
#################################################################

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)
parser.add_argument('due_date', type=date_time_parsing)

class TodoListResource(Resource):

    @jwt_required
    def post(self):
        data = parser.parse_args()
        data['user_id'] = get_jwt_identity()
        todo = Todo.create_todo(data)
        return marshal(todo, resource_fields)


#################################################################
# TodoListResource
# lets you GET a list of completed todos
#################################################################

class CompletedTodoListResource(Resource):
    @jwt_required
    @marshal_with(resource_fields)
    def get(self):
        user_id = get_jwt_identity()
        todos = Todo.query \
            .by_owner(user_id) \
            .completed().all()
        return todos


#################################################################
# TodoListResource
# lets you GET a list of completed todos
#################################################################

class UnCompletedTodoListResource(Resource):
    @jwt_required
    @marshal_with(resource_fields)
    def get(self):
        user_id = get_jwt_identity()
        todos = Todo.query \
            .by_owner(user_id) \
            .uncompleted().all()
        return todos
