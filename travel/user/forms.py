from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_login import current_user
from .models import User

class UserRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=7)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')]) 
    submit = SubmitField('Sign up') 
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken! Please use another one.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken! Please use another one.')

class UserLoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=7)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    password = PasswordField('Password', validators=[Length(min=7)])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password', message='Passwords must match')]) 
    submit = SubmitField('Update Account') 

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken! Please use another one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken! Please use another one.')

class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[Length(min=7)])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password', message='Passwords must match')]) 
    submit = SubmitField('Change Password') 

class AddCommentForm(FlaskForm):
    text = TextAreaField('Comment Something!')
    submit = SubmitField('Add comment') 