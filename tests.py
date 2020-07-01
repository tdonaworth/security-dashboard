from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Task

class UserModelCase(unittest.TestCase):
    def setUp(self):
        current_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

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