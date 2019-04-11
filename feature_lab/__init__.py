from flask import Flask
from feature_lab.main.routes import main
from feature_lab.clients.routes import clients


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '5a2cf7b4d5d6bdb18f30487b340a81fd'

    app.register_blueprint(main)
    app.register_blueprint(clients)

    return app
