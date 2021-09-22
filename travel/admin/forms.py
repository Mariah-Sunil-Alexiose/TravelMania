from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import Admin

class AdminRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=7)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')]) 
    key = IntegerField(' Admin Key')
    submit = SubmitField('Sign up') 
    
    def validate_username(self, username):
        user = Admin.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken! Please use another one.')

    def validate_email(self, email):
        email = Admin.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken! Please use another one.')


class AdminLoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=7)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')