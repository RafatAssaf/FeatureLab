import unittest
from flask_bcrypt import Bcrypt
from feature_lab import create_app, db
from feature_lab.models import User
from sqlalchemy.exc import IntegrityError


class UserModelTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_password = 'testing123_$%'

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.bcrypt = Bcrypt(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_username_value(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        username = 'Will Smith'
        u = User(username, 'will@demo.com', pw)
        db.session.add(u)
        db.session.commit()
        self.assertTrue(u.username == username)

    def test_username_value_null(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        username = None
        u = User(username, 'will@demo.com', pw)
        with self.assertRaises(IntegrityError):
            db.session.add(u)
            db.session.commit()

    def test_email_value(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        email = 'will@demo.com'
        u = User('Will Smith', email, pw)
        db.session.add(u)
        db.session.commit()
        self.assertTrue(u.email == email)

    def test_email_value_null(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        email = None
        u = User('Will Smith', email, pw)
        with self.assertRaises(IntegrityError):
            db.session.add(u)
            db.session.commit()

    def test_password_hash_check(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        u = User('Will Smith', 'will@demo.com', pw)
        db.session.add(u)
        db.session.commit()
        q_u = User.query.first()
        self.assertTrue(self.bcrypt.check_password_hash(q_u.password, self.test_password))

    def test_id_not_repeated(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        u1 = User('Will Smith', 'will@demo.com', pw)
        u2 = User('Johnny Depp', 'depp@demo.com', pw)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        q_u1 = User.query.get(u1.id)
        q_u2 = User.query.get(u2.id)
        self.assertFalse(q_u1.id == q_u2.id)

    def test_username_must_be_unique(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        u1 = User('Will Smith', 'will@demo.com', pw)
        u2 = User('Will Smith', 'will2@demo.com', pw)
        db.session.add(u1)
        db.session.add(u2)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_email_must_be_unique(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        u1 = User('Will Smith', 'will@demo.com', pw)
        u2 = User('Will Smith2', 'will@demo.com', pw)
        db.session.add(u1)
        db.session.add(u2)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_user_clients(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        u = User('Will Smith', 'will@demo.com', pw)
        db.session.add(u)
        db.session.commit()
        q_u = User.query.get(u.id)
        self.assertListEqual(q_u.clients, [])
