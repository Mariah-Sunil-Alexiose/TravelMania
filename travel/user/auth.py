from flask import render_template, Blueprint, request, flash, redirect, url_for, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from travel import db, photos, login_manager
from flask_login import login_required, current_user, logout_user, login_user
from .forms import UserRegistrationForm, UserLoginForm
from .models import User
import secrets, os

user_auth = Blueprint('user_auth', __name__)

@user_auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = generate_password_hash(form.password.data, method='sha256')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome User {form.name.data}! Thank you for registering!', 'success')
        return redirect(url_for('user_auth.login'))
    return render_template('user/signup.html', form=form, user=current_user)

@user_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Welcome User {user.username}! You are logged in!', 'success')
            return redirect(request.args.get('next') or url_for('views.explore'))
        else:
            flash('Wrong Email or Password! Please try again!', 'danger')
    return render_template('user/login.html', form=form, user=current_user)

@user_auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('user_auth.login'))