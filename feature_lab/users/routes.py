from flask import Blueprint, render_template, flash, redirect, url_for
from feature_lab.users.forms import LoginForm, SignupForm
from feature_lab import bcrypt, db
from feature_lab.models import User
from flask_login import login_user, current_user, logout_user
users = Blueprint('users', __name__)


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember.data)
            flash('Welcome back, {}!'.format(user.username), 'info')
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful, Please check your email and password', 'danger')
    return render_template('login.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))