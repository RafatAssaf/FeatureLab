from flask import Flask
from feature_lab.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    # app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    # importing those after initializing db with app
    from feature_lab.main.routes import main
    from feature_lab.clients.routes import clients
    from feature_lab.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(clients)
    app.register_blueprint(users)

    return app
