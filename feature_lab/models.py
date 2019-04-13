# from flask import current_app
from feature_lab import db
from datetime import datetime
import enum


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "User({}), with ID: {}, and email: {}".format(self.username, self.id, self.email)

    def __init__(self,
                 username,
                 email,
                 password):
        self.username = username
        self.email = email
        self.password = password


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.Text(), nullable=False)
    phone_number = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    products = db.relationship('Product', backref='owner', lazy=True)

    def __repr__(self):
        return "Client ({}), Created At: {}, with ID: {}".format(self.name, self.created_at, self.id)

    def __init__(self,
                 name,
                 email,
                 bio,
                 phone_number):
        self.name = name
        self.email = email
        self.bio = bio
        self.phone_number = phone_number


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    #  requests relationship
    areas = None

    def __repr__(self):
        return 'Product({}), of ID: {}'.format(self.name, self.id)

    def __init__(self,
                 name,
                 description,
                 owner_id,
                 areas_string):
        self.name = name
        self.description = description
        self.owner_id = owner_id

        class Areas(enum.Enum):
            def __init__(self):
                areas_names = areas_string.split(',')
                for area in areas_names:
                    self[area] = area

        self.areas = db.Column(db.Enum(Areas))


class FeatureRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    target_date = db.Column(db.DateTime, nullable=False)
    product_area = db.Column(db.String())
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return 'Request ({}), of ID: {}'.format(self.title, self.id)

    def __init__(self,
                 title,
                 description,
                 priority,
                 created_at,
                 target_date,
                 product_area,
                 product_id):
        self.title = title
        self.description = description
        self.priority = priority
        self.created_at = datetime.strptime(created_at, '%Y-%m-%d')
        self.target_date = datetime.strptime(target_date, '%Y-%m-%d')
        self.product_area = product_area
        self.product_id = product_id
