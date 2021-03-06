import json
from flask import Blueprint, abort, make_response

from flask_restful import (Api, fields, reqparse,
                           marshal, marshal_with, Resource, url_for)

import models

"""
configuring fields
"""
todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'created_at': fields.DateTime
}


def todo_or_404(id):
    try:
        todo = models.Todo.get(models.Todo.id == id)
    except models.Todo.DoesNotExist:
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
        """Get todos"""
        todos = [marshal(todo, todo_fields)
                 for todo in models.Todo.select()]
        return todos

    @marshal_with(todo_fields)
    def post(self):
        """Create todo"""
        args = self.reqparse.parse_args()
        todo = models.Todo.create(**args)
        return (todo, 201,
            {'Location': url_for('resources.todos.todo', id=todo.id)}
        )


class Todo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No name provided',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self, id):
        """Get single todo"""
        return todo_or_404(id)

    @marshal_with(todo_fields)
    def put(self, id):
        """Update todo"""
        args = self.reqparse.parse_args()
        query = models.Todo.update(**args).where(models.Todo.id==id)
        query.execute()
        return (models.Todo.get(models.Todo.id==id), 200,
            {'Location': url_for('resources.todos.todo', id=id)}
        )

    @marshal_with(todo_fields)
    def delete(self, id):
        """Delete todo"""
        try:
            todo = models.Todo.get(models.Todo.id==id)
        except models.Todo.DoesNotExist:
            return make_response(json.dumps(
                    {'error': 'That review does not exist or is not editable'}
                ), 403)
        todo.delete_instance()
        return '', 204, {'Location': url_for('resources.todos.todos')}


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
