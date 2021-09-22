from flask import Flask
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_login import LoginManager
import os

db = SQLAlchemy()
DB_NAME = "travel.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config["UPLOADED_PHOTOS_DEST"] = "travel/static/img"
app.config["SECRET_KEY"] = os.urandom(24)
photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='user_auth.login'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message = u'Please login first'
login_manager.login_message_category = "danger"

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

from .admin.auth import admin_auth
from .admin.views import admin_views

app.register_blueprint(admin_auth, url_prefix='/admin')
app.register_blueprint(admin_views, url_prefix='/admin')

from .admin.models import Admin

from .user.auth import user_auth
from .user.views import user_views
from .user.models import User, Note, Bookmark, Post, Comment, Like

app.register_blueprint(user_auth, url_prefix='/user')
app.register_blueprint(user_views, url_prefix='/user')

from .countries.models import Country, Continent, Leisure, Landmarks

from .countries.views import views
app.register_blueprint(views, url_prefix='/')

def create_database(app):
    if not path.exists('travel/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

create_database(app)