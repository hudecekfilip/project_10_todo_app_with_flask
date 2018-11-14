import unittest
import json
from peewee import *
from datetime import datetime

from app import app
from models import Todo

MODELS = [Todo]

test_db = SqliteDatabase(':memory:')


class ViewTests(unittest.TestCase):
    def setUp(self):
        """
        Creating testing DB
        """
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        Todo.create(name="TestTODO")

    def tearDown(self):
        """
         Deleting testing DB
         """
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_homepage(self):
        """
        Testing if homepage exists
        """
        app.config['TESTING'] = True
        self.app = app.test_client()
        homeview = self.app.get('/')
        self.assertEqual(homeview.status_code, 200)

    def test_todos_page(self):
        """
        Testing if todos are displayed
        """
        app.config['TESTING'] = True
        self.app = app.test_client()
        todos_view = self.app.get('/api/v1/todos')
        self.assertEqual(todos_view.status_code, 200)


class TodoModel(unittest.TestCase):
    def setUp(self):
        """
        Creating testing DB
        """
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        Todo.create(name="TestTODO", created_at='2000-01-01')

    def tearDown(self):
        """
        Deleting testing DB
        """
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_todo_model(self):
        """
        Testing if TODO has been successfully created
        """
        dt = datetime(2000, 1, 1, 0, 0)
        self.assertEqual(Todo.get(Todo.name == 'TestTODO').name, 'TestTODO')
        self.assertEqual(Todo.get(Todo.created_at == '2000-01-01').created_at, dt)

    def test_todo_post(self):
        app.config['TESTING'] = True
        self.app = app.test_client()


class TodoClass(unittest.TestCase):
    def setUp(self):
        """
        Creating testing DB
        """
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        Todo.create(name="TestTODO", created_at='2000-01-01')

    def tearDown(self):
        """
        Deleting testing DB
        """
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_get_todo_list(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        Todo.create(name='TODO')
        listview = self.app.get('/api/v1/todos')
        self.assertEqual(listview.status_code, 200)
        self.assertEqual(Todo.get(Todo.name == 'TODO').name, 'TODO')

    def test_delete(self):
        """
        Test delete todo
        """
        app.config['TESTING'] = True
        self.app = app.test_client()
        delete = self.app.delete('/api/v1/todos/1')
        self.assertEqual(delete.status_code, 204)


if __name__ == '__main__':
    unittest.main()
