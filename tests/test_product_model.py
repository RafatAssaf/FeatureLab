import unittest
from flask_bcrypt import Bcrypt
from feature_lab import create_app, db
from feature_lab.models import User, Client, Product, FeatureRequest
from sqlalchemy.exc import IntegrityError


class ProductModelTestCase(unittest.TestCase):
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
        self.test_client = Client("Company X",
                                  'companyx@demo.com',
                                  'bio text goes here, bio text goes here',
                                  1, '7176577957', self.test_user.id)
        db.session.add(self.test_client)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_product_values(self):
        p = Product('Prod-X',
                    'Product Description',
                    self.test_client.id)
        db.session.add(p)
        db.session.commit()
        q_p = Product.query.get(p.id)
        self.assertEqual(q_p.name, p.name)
        self.assertEqual(q_p.description, p.description)
        self.assertEqual(q_p.owner_id, p.owner_id)

    def test_name_null(self):
        p = Product(None,
                    'Product Description',
                    self.test_client.id)
        db.session.add(p)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_description_null(self):
        p = Product('Prod-X',
                    None,
                    self.test_client.id)
        db.session.add(p)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_client_id_null(self):
        p = Product('Prod-X',
                    'Product Description',
                    None)
        db.session.add(p)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_product_requests(self):
        p = Product('Prod-X',
                    'Product Description',
                    self.test_client.id)
        db.session.add(p)
        db.session.commit()
        q_p = Product.query.get(p.id)
        self.assertListEqual(q_p.requests, [])
        self.assertTrue(FeatureRequest.query.filter_by(product_id=q_p.id).count() == 0)
