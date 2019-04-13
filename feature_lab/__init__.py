from flask import Flask
from feature_lab.main.routes import main
from feature_lab.clients.routes import clients
from feature_lab.config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(clients)

    return app
