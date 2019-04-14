from flask import Blueprint, render_template, flash, redirect, url_for
from feature_lab.users.forms import LoginForm, SignupForm
from feature_lab import bcrypt, db
from feature_lab.models import User
users = Blueprint('users', __name__)


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(form.username.data,
                    form.email.data,
                    hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('An account for {} has been created! You can now login to your account'.format(form.username.data), 'success')
        return redirect(url_for('users.login'))
    return render_template('signup.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if True:
            flash('Welcome back, <username>!', 'info')
            return redirect(url_for('main.home'))
    return render_template('login.html', form=form)
