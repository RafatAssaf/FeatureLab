import unittest
from feature_lab import create_app, db
from flask_wtf.csrf import generate_csrf
from feature_lab.models import User


class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.test_client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_signup(self):
        r = self.test_client.get('/signup')
        # did the request fail?
        self.assertEqual(r.status_code, 200)
        # did we get the expected page?
        self.assertTrue("Create Account" in r.get_data(as_text=True))
        user_data = {
            'csrf_token': generate_csrf(),
            'username': 'Rafat Assaf',
            'email': 'rafat@demo.com',
            'password': 'testing',
            'confirm_password': 'testing'
        }
        # try to POST a user into the database
        r = self.test_client.post('/signup', data=user_data, follow_redirects=True)
        q_u = User.query.filter_by(username=user_data['username']).first()
        # did the request fail?
        self.assertEqual(r.status_code, 200)
        # did it actually create the user?
        self.assertIsNotNone(q_u)

    def test_login(self):
        self.test_client.get('/signup')
        user_data = {
            'csrf_token': generate_csrf(),
            'username': 'Rafat Assaf',
            'email': 'rafat@demo.com',
            'password': 'testing',
            'confirm_password': 'testing'
        }
        # register the user
        self.test_client.post('/signup', data=user_data, follow_redirects=True)
        # request login page
        r = self.test_client.get('/login')
        # was the request successful?
        self.assertEqual(r.status_code, 200)
        # did we get the expected page?
        self.assertTrue('<legend class="border-bottom mb-4">Log In</legend>' in r.get_data(as_text=True))
        # login the user
        r = self.test_client.post('/login', data=user_data, follow_redirects=True)
        # was the request successful?
        self.assertEqual(r.status_code, 200)
        # did we get the expected page?
        self.assertTrue('Welcome back,' in r.get_data(as_text=True))
        # check if the user authenticated
        u_q = User.query.filter_by(email=user_data['email']).first()
        self.assertTrue(u_q.is_authenticated)