from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from travel import db
from .forms import AdminRegistrationForm, AdminLoginForm
from .models import Admin

admin_auth = Blueprint('admin_auth', __name__)

@admin_auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = AdminRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = generate_password_hash(form.password.data, method='sha256')
        admin = Admin(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password)
        if form.key.data == 123:
            db.session.add(admin)
            db.session.commit()
            flash(f'Welcome Administer {form.name.data}! Thank you for registering!', 'success')
            return redirect(url_for('admin_views.index'))
        else: 
            flash('You are not authorized to signup', 'danger')
            return redirect(url_for('admin_auth.signup'))
    return render_template('admin/signup.html', form=form)

@admin_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = AdminLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and check_password_hash(admin.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome Administer {admin.username}! You are logged in!', 'success')
            return redirect(request.args.get('next') or url_for('admin_views.index'))
        else:
            flash('Wrong Email or Password! Please try again!', 'danger')
    return render_template('admin/login.html', form=form)

@admin_auth.route('/logout')
def logout():
    if 'email' in session:
        flash('You are logged out!', 'info')
        return redirect(url_for('admin_auth.login'))