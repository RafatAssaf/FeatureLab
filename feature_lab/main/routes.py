from flask import Blueprint, request, render_template

main = Blueprint('main', __name__)

requests = [
    {'name': "request 1"},
    {'name': "request 2"},
    {'name': "request 3"},
    {'name': "request 4"},
]


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', requests=requests, title='Home')
