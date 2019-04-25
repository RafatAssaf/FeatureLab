from datetime import datetime
from feature_lab import create_app, db
from flask_bcrypt import Bcrypt
from feature_lab.models import User, Client, Product, ProductArea, FeatureRequest

app = create_app()
app.app_context().push()
bcrypt = Bcrypt(app)

db.drop_all()
db.create_all()

# create a user
user = User('Rafat Assaf',
            'rafat@demo.com',
            bcrypt.generate_password_hash('Testing123$'))

db.session.add(user)
db.session.commit()

# create clients
client_1 = Client('Kings Landing solutions',
                  'lannister@demo.com',
                  'Technical solutions across all of Westeros',
                  '92387471989', user.id)
client_2 = Client('Winterfell solutions',
                  'stark@demo.com',
                  'Technical solutions across all of the world',
                  '74897928191', user.id)

db.session.add(client_1)
db.session.add(client_2)
db.session.commit()

# create products
product_1 = Product('Mobile App', 'The official Lannister mobile app', client_1.id)
product_2 = Product('Website', 'The official Lannister website', client_1.id)
product_3 = Product('Machine learning model', 'An ML model that predicts the amount of white walkers after a given amount of battles', client_2.id)

db.session.add(product_1)
db.session.add(product_2)
db.session.add(product_3)
db.session.commit()

# create product areas
areas = [
    ProductArea('User Profile', product_1.id),
    ProductArea('Search', product_1.id),
    ProductArea('Home Page', product_2.id),
    ProductArea('SEO', product_2.id),
    ProductArea('Data Pipeline', product_3.id),
    ProductArea('Neural Network', product_3.id),
    ProductArea('Model Deployment', product_3.id),
]

for area in areas:
    db.session.add(area)
db.session.commit()

# create feature requests
requests = [
    FeatureRequest('Edit profile',
                   'Add the ability to edit profile',
                   datetime.utcnow(),
                   datetime(2019, 8, 15),
                   areas[0].name,
                   product_1.id,
                   client_1.id, 1),
    FeatureRequest('Elastic Search',
                   'Setup and utilize Elastic Search',
                   datetime.utcnow(),
                   datetime(2019, 12, 1),
                   areas[1].name,
                   product_1.id,
                   client_1.id, 2),
    FeatureRequest('Create pipeline',
                   'Create the data pipeline for the model',
                   datetime.utcnow(),
                   datetime(2019, 5, 27),
                   areas[4].name,
                   product_3.id,
                   client_2.id, 1),
    FeatureRequest('Implement Neural Network',
                   'Implement the neural network using Keras',
                   datetime.utcnow(),
                   datetime(2019, 6, 12),
                   areas[5].name,
                   product_3.id,
                   client_2.id, 2),
    FeatureRequest('Train NN',
                   'Train the neural network on training data, not on testing data!!',
                   datetime.utcnow(),
                   datetime(2019, 7, 7),
                   areas[6].name,
                   product_3.id,
                   client_2.id, 3)
]

for request in requests:
    db.session.add(request)
db.session.commit()
