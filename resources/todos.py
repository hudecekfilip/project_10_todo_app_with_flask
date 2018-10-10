import json
from flask import jsonify, Blueprint, abort, make_response

from flask_restful import (Api, fields, reqparse,
                        marshal, marshal_with, Resource)


import models


todos_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'created_at': fields.DateTime
}

def todo_or_404(review_id):
    try:
        todo = models.Todo.get(models.Todo.id==todo_uid)
    except models.Review.DoesNotExist:
        abort(404)
    else:
        return todo


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No name provided',
            location=['form', 'json']
        )
        super().__init__()


    def get(self):
        todos = [marshal(todo, todos_fields)
                    for todo in models.Todo.select()]
        return {'todos': todos}

    @marshal_with(todos_fields)
    def post(self):
        args = self.reqparse.parse_args()
        todo = models.Todo.create(
                created_by=g.user,
                **args
        )
        return (todo,
                201,
                {'Location': url_for('resources.reviews.review', id=review.id)}
                )


class Todo(Resource):
    @marshal_with(todos_fields)
    def get(self, id):
        return todo_or_404(id)


todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)
api.add_resource(
    TodoList,
    '/api/v1/todos',
    endpoint='todos'
)
api.add_resource(
    Todo,
    '/api/v1/todos/<int:id>',
    endpoint='todo'
)
