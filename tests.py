#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Task
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        u = User(username='sam', email='sam@email.com')
        u.set_password('foobar')
        db.session.add(u)
        db.session.commit()
        q = User.query.filter_by(username=u.username).first()
        self.assertTrue(q is not None)

    def test_password_hashing(self):
        u = User(username='sam')
        u.set_password('foobar')
        self.assertFalse(u.check_password('barfoo'))
        self.assertTrue(u.check_password('foobar'))

if __name__ == '__main__':
    unittest.main(verbosity=2)