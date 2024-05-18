# import os
# os.environ['DATABASE_URL'] = 'sqlite://'

# from datetime import datetime, timezone, timedelta
import unittest
from app import create_app, db
from config import TestConfig
from app.models import Trade, User
from unittest import TestCase

class UserModelCase(TestCase):
    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        
        db.create_all()
        # add_test_data_to_db()
        
        # Create a user for testing
        self.user = User(username='testuser', email='testuser@example.com')
        self.user.set_password('testpassword')
        db.session.add(self.user)
        db.session.commit()

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

    def test_all_trades(self):
        # Create another user and some trades for testing
        user2 = User(username='testuser2', email='testuser2@example.com')
        db.session.add(user2)
        db.session.commit()

        trade1 = Trade(user_id1=self.user.id, user_id2=user2.id, pokemon_id1=1, pokemon_id2=2)
        trade2 = Trade(user_id1=user2.id, user_id2=self.user.id, pokemon_id1=3, pokemon_id2=4)
        db.session.add_all([trade1, trade2])
        db.session.commit()

        trades = self.user.all_trades()
        self.assertEqual(len(trades), 2)
    
    def test_accepted_trades(self):
        user2 = User(username='testuser2', email='testuser2@example.com')
        db.session.add(user2)
        db.session.commit()

        trade1 = Trade(user_id1=user2.id, user_id2=self.user.id, pokemon_id1=1, pokemon_id2=2)
        trade2 = Trade(user_id1=user2.id, user_id2=self.user.id, pokemon_id1=3, pokemon_id2=4)
        db.session.add_all([trade1, trade2])
        db.session.commit()

        accepted_trades = self.user.accepted_trades()
        self.assertEqual(len(accepted_trades), 2)
if __name__ == '__main__':
    unittest.main(verbosity=2)

