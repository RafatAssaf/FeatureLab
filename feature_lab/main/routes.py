from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from feature_lab.models import FeatureRequest, Client

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    user_clients = Client.query.filter_by(user_id=current_user.id).all()
    requests = []
    for client in user_clients:
        client_requests = FeatureRequest.query.filter_by(client_id=client.id).all()
        requests += client_requests
    return render_template('home.html', requests=requests, title='Home')


@main.route('/about')
def about():
    return render_template('about.html', title='About')
