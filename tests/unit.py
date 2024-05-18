# import os
# os.environ['DATABASE_URL'] = 'sqlite://'

# from datetime import datetime, timezone, timedelta
import unittest
from app import create_app, db
from config import TestConfig
from app.models import User
from unittest import TestCase

class UserModelCase(TestCase):
    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        
        db.create_all()
        # add_test_data_to_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan', email='susan@example.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

if __name__ == '__main__':
    unittest.main(verbosity=2)

