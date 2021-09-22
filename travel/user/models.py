from travel import db
from sqlalchemy.sql import func
from flask_login import UserMixin 

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(50))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', backref=db.backref('post_user',overlaps="post_user,user", lazy=True))

    country_id = db.Column(db.Integer, db.ForeignKey('country.id', ondelete="CASCADE"), nullable=False)
    country = db.relationship('Country', backref=db.backref('post_country',overlaps="country,post_country", lazy=True))

    comments = db.relationship('Comment', backref='post_comment',overlaps="comments,post_comment", passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_user',overlaps="comment_user,user", lazy=True))

    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
    post = db.relationship('Post', backref=db.backref('comment_post',overlaps="comments,post_comment", lazy=True))

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    avatar = db.Column(db.String(20), default='avatar.png', nullable=False)
    notes = db.relationship('Note')
    bookmarks = db.relationship('Bookmark')
    posts = db.relationship('Post')
    comments = db.relationship('Comment')
    likes = db.relationship('Like', backref='user', passive_deletes=True)

    def __repr__(self):
        return '<User %r>' % self.username