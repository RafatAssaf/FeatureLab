from flask import Blueprint, render_template, flash, redirect, url_for
from feature_lab.users.forms import LoginForm, SignupForm
from feature_lab import bcrypt, db
from feature_lab.models import User, Client, Product, FeatureRequest, FeatureRequestState
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


@users.route('/profile')
def profile():
    # list of statistics for each client
    profile_stats = []
    user_clients = Client.query.filter_by(user_id=current_user.id)
    for client in user_clients:
        client_data = {
            'name': client.name,
            'products': []
        }
        for product in client.products:
            num_resolved = FeatureRequest.query\
                .filter_by(state=FeatureRequestState.RESOLVED, product_id=product.id).count()
            num_open = FeatureRequest.query\
                .filter_by(product_id=product.id).filter(FeatureRequest.state != FeatureRequestState.RESOLVED).count()
            num_all = FeatureRequest.query.filter_by(product_id=product.id).count()
            ratio_done = num_resolved / num_all if num_all > 0 else 0
            client_data['products'].append({
                'name': product.name,
                'num_resolved': num_resolved,
                'num_open': num_open,
                'ratio_done': ratio_done
            })
        profile_stats.append(client_data)
    return render_template('profile.html', user=current_user, profile_stats=profile_stats)


# @users.route('/profile/update'):
# def update_profile():
#     form = SignupForm()
