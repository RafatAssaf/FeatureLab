import unittest
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from feature_lab import create_app, db
from feature_lab.models import User, Client, Product, FeatureRequest, ProductArea
from sqlalchemy.exc import IntegrityError


class FeatureRequestModelTestCase(unittest.TestCase):
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
        self.test_product = Product('Product-A', 'Product Desciption', self.test_client.id)
        db.session.add(self.test_product)
        db.session.commit()
        pa1 = ProductArea('Area1', self.test_product.id)
        pa2 = ProductArea('Area2', self.test_product.id)
        db.session.add(pa1)
        db.session.add(pa2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_request_values(self):
        a = ProductArea.query.filter_by(product_id=self.test_product.id).first()
        fr = FeatureRequest('Request title',
                            'request description',
                            datetime.utcnow(),
                            datetime(2019,8,15),
                            a.name,
                            self.test_product.id,
                            self.test_client.id)
        db.session.add(fr)
        db.session.commit()
        q_fr = FeatureRequest.query.get(fr.id)
        self.assertEqual(q_fr.title, fr.title)
        self.assertEqual(q_fr.description, fr.description)
        self.assertEqual(q_fr.created_at, fr.created_at)
        self.assertEqual(q_fr.target_date, fr.target_date)
        self.assertEqual(q_fr.product_area, fr.product_area)
        self.assertEqual(q_fr.product_id, fr.product_id)
        self.assertEqual(q_fr.client_id, fr.client_id)

    def test_request_initial_state(self):
        a = ProductArea.query.filter_by(product_id=self.test_product.id).first()
        fr = FeatureRequest('Request title',
                            'request description',
                            datetime.utcnow(),
                            datetime(2019, 8, 15),
                            a.name,
                            self.test_product.id,
                            self.test_client.id)
        db.session.add(fr)
        db.session.commit()
        q_fr = FeatureRequest.query.get(fr.id)
        self.assertEqual(q_fr.state.name, 'TODO')

    def test_requests_relationships(self):
        a = ProductArea.query.filter_by(product_id=self.test_product.id).first()
        fr = FeatureRequest('Request title',
                            'request description',
                            datetime.utcnow(),
                            datetime(2019, 8, 15),
                            a.name,
                            self.test_product.id,
                            self.test_client.id)
        db.session.add(fr)
        db.session.commit()
        q_fr = FeatureRequest.query.get(fr.id)
        self.assertTrue(FeatureRequest.query.filter_by(product_id=self.test_product.id).count() == 1)
        self.assertEqual(q_fr.product, self.test_product)
