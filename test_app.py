import unittest
from app import app, db, Task

class TaskApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_create_task(self):
        response = self.client.post('/api/tasks', json={
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'Pending',
            'important': False
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_get_tasks(self):
        with app.app_context():
            db.session.add(Task(title='Task1'))
            db.session.commit()
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_update_task(self):
        with app.app_context():
            t = Task(title='Task2')
            db.session.add(t)
            db.session.commit()
            tid = t.id
        response = self.client.put(f'/api/tasks/{tid}', json={'title': 'Updated'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.get_json())

    def test_delete_task(self):
        with app.app_context():
            t = Task(title='Task3')
            db.session.add(t)
            db.session.commit()
            tid = t.id
        response = self.client.delete(f'/api/tasks/{tid}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.get_json())

if __name__ == '__main__':
    unittest.main()
