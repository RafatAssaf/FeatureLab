from flask import Blueprint, render_template, flash, redirect, url_for
from feature_lab.users.forms import LoginForm
users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if True:
            flash('Welcome back, <username>!', 'info')
            return redirect(url_for('main.home'))
    return render_template('login.html', form=form)