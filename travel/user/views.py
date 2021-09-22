from flask import render_template, Blueprint, url_for, request, flash, redirect, session, jsonify
from werkzeug.security import generate_password_hash
from travel import db, app
from flask_login import current_user, login_required
from .forms import UpdateAccountForm, ChangePasswordForm, AddCommentForm
from travel.countries.models import Country
from .models import User, Bookmark, Note, Post, Comment, Like
import secrets, os, json

user_views = Blueprint('user_views', __name__)

@login_required
@user_views.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('user_views.posts', username=current_user.username))
    
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/avatar', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@login_required
@user_views.route('/profile', methods=['GET', 'POST'])
def profile():
    form = UpdateAccountForm()
    if request.method == 'POST':
        if form.image.data:
            picture_file = save_picture(form.image.data)
            current_user.avatar = picture_file
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account information has been updated!', 'success')
        return redirect(url_for('user_views.profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/avatar/' + current_user.avatar)
    return render_template('user/profile.html', user=current_user, image_file=image_file, form=form)

@login_required
@user_views.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password.data, method='sha256')
        current_user.password = hash_password
        db.session.commit()
        flash('Your account information has been updated!', 'success')
        return redirect(url_for('user_views.change_password'))
    return render_template('user/change_password.html', user=current_user, form=form)

@login_required
@user_views.route('/bookmarks')
def bookmarks():
    bookmark=Bookmark.query.order_by(Bookmark.id.desc()).all()
    return render_template("user/bookmarks.html", user=current_user, bookmark=bookmark)

@user_views.route('/bookmarks/<name>')
@login_required
def newbookmark(name):
    count = Bookmark.query.filter_by(country=name,user_id=current_user.id).count()
    if count == 0:
        bookmark = Bookmark(country=name,user_id=current_user.id)
        db.session.add(bookmark)
        db.session.commit()
        flash('The country is added to Bookmarks!', 'success')
    else:
        flash('The bookmark already exists!', 'success')
    bookmark=Bookmark.query.order_by(Bookmark.id.desc()).all()
    return render_template("user/bookmarks.html", user=current_user, bookmark=bookmark)

@user_views.route('/deletebookmark/<int:id>', methods=['POST'])
@login_required
def deletebookmark(id):
    if request.method == 'POST':
        bookmark = Bookmark.query.get(id)
        db.session.delete(bookmark)
        db.session.commit()
        flash('The bookmark is deleted', 'success')
    bookmark=Bookmark.query.order_by(Bookmark.id.desc()).all()
    return render_template("user/bookmarks.html", user=current_user)

@user_views.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Checklist Item is too short!', 'danger')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Item added!', 'success')

    return render_template("user/todo.html", user=current_user)

@login_required
@user_views.route('/delete_todo', methods=['POST'])
def delete_todo():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@user_views.route("/create_post/<id>", methods=['GET', 'POST'])
@login_required
def create_post(id):
    countries = Country.query.all()
    if request.method == "POST":
        text = request.form.get('text')
        if not text:
            flash('Post cannot be empty', 'danger')
        else:
            post = Post(text=text, user_id=current_user.id, country_id=id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', 'success')
            return redirect(request.args.get('next') or url_for('user_views.country_posts', id=id))
    return render_template('user/create_post.html', user=current_user, countries=countries)

@user_views.route("/delete_post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist!", 'danger')
    elif post.comments == 0:
        flash('You cannot delete a post if there are comments!', 'danger')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted!', 'success')
    return redirect(url_for('user_views.index'))

@user_views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('No user with that username exists!', 'danger')
        return redirect(url_for('user_views.index'))
    posts = user.posts
    return render_template("user/posts.html", user=current_user, posts=posts, username=username)

@user_views.route("/country/posts/<id>")
@login_required
def country_posts(id):
    country = Country.query.filter_by(id=id).first()
    if not country:
        flash('Country does not exist!', 'error')
        return redirect(request.args.get('next') or url_for('views.getcountry', id=id))
    posts = country.posts
    return render_template("user/posts.html", user=current_user, posts=posts, id=id, username=None)

@user_views.route("/create_comment/<post_id>", methods=['GET','POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')
    if not text:
        flash('Comment cannot be empty.', 'danger')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text, user_id=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist!', 'danger')
    return redirect(url_for('user_views.index'))


@user_views.route("/delete_comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('Comment does not exist.', 'danger')
    elif current_user.id != comment.user_id and current_user.id != comment.post.user_id:
        flash('You do not have permission to delete this comment!', 'danger')
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('user_views.index'))