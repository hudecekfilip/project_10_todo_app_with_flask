import json
from flask import jsonify, Blueprint, abort, make_response

from flask_restful import (Api, fields, reqparse,
                        marshal, marshal_with, Resource, url_for)


import models


todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'created_at': fields.DateTime
}

def todo_or_404(id):
    try:
        todo = models.Todo.get(models.Todo.id==id)
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
        todos = [marshal(todo, todo_fields)
                    for todo in models.Todo.select()]
        return {'todos': todos}

    @marshal_with(todo_fields)
    def post(self):
        args = self.reqparse.parse_args()
        todo = models.Todo.create(**args)
        return (todo,
                201,
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
        print("ID:".format(id))
        return todo_or_404(id)

    @marshal_with(todo_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        try:
            todo = models.Todo.select().where(
                models.Todo.id==id
            ).get()
        except models.Todo.DoesNotExist:
            return make_response(json.dumps(
                    {'error': 'That review does not exist or is not editable'}
                ), 403)
        query = todo.update(**args)
        query.execute()
        todo = todo_or_404(id)
        return (todo, 200, {
                'Location': url_for('resources.todos.todo', id=id)
               })

    @marshal_with(todo_fields)
    def delete(self, id):
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
