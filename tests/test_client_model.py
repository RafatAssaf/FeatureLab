import unittest
from flask_bcrypt import Bcrypt
from feature_lab import create_app, db
from feature_lab.models import User, Client
from sqlalchemy.exc import IntegrityError


class ClientModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.bcrypt = Bcrypt(self.app)
        db.create_all()
        self.test_user = User('Will Smith', 'will@demo.com',
                              self.bcrypt.generate_password_hash('testing123_$%').decode('utf-8'))
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_client_values(self):
        c = Client("Company X",
                   'companyx@demo.com',
                   'bio text goes here, bio text goes here',
                   1, '7176577957', self.test_user.id)
        db.session.add(c)
        db.session.commit()
        q_c = Client.query.get(c.id)
        self.assertTrue(c.name == q_c.name)
        self.assertTrue(c.email == q_c.email)
        self.assertTrue(c.bio == q_c.bio)
        self.assertTrue(c.priority == q_c.priority)
        self.assertTrue(c.created_at == q_c.created_at)
        self.assertTrue(c.user_id == q_c.user_id)

    def test_name_value_null(self):
        c = Client(None,
                   'companyx@demo.com',
                   'bio text goes here, bio text goes here',
                   1, '7176577957', self.test_user.id)
        db.session.add(c)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_email_value_null(self):
        c = Client("Company X",
                   None,
                   'bio text goes here, bio text goes here',
                   1, '7176577957', self.test_user.id)
        db.session.add(c)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_bio_value_null(self):
        c = Client("Company X",
                   'companyx@demo.com',
                   None,
                   1, '7176577957', self.test_user.id)
        db.session.add(c)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_priority_value_null(self):
        c = Client("Company X",
                   'companyx@demo.com',
                   'bio text goes here, bio text goes here',
                   None, '7176577957', self.test_user.id)
        db.session.add(c)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_user_id_value_null(self):
        c = Client("Company X",
                   'companyx@demo.com',
                   'bio text goes here, bio text goes here',
                   1, '7176577957', None)
        db.session.add(c)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_user_ref(self):
        c = Client("Company X",
                   'companyx@demo.com',
                   'bio text goes here, bio text goes here',
                   1, '7176577957', self.test_user.id)
        db.session.add(c)
        db.session.commit()
        q_c = Client.query.get(c.id)
        self.assertIsInstance(q_c.user, User)

    def test_client_products(self):
        c = Client("Company X",
                   'companyx@demo.com',
                   'bio text goes here, bio text goes here',
                   1, '7176577957', self.test_user.id)
        db.session.add(c)
        db.session.commit()
        q_c = Client.query.get(c.id)
        self.assertListEqual(q_c.products, [])
