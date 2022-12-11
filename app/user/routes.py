from datetime import datetime

from flask import redirect, url_for, flash, request, render_template, current_app
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message
from werkzeug.urls import url_parse

from app import db
from app.user import bp
from app.user.forms import LoginForm, RegisterForm, EditAccountForm
from app.models import User, Post


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('user.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next_page')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user.account')
        return redirect(next_page)
    return render_template('user/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Success! Your account has been registered')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', title='Registration', form=form)


@bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user = User.query.filter_by(username=current_user.username).first()
    post = Post.query.all()
    users = User.query.all()
    form = EditAccountForm()
    # if nothing is entered -->
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # if userdata is entered -->
    elif form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Success! Your account has been edited')
        return redirect(url_for('user.account'))
    current_user.last_seen = datetime.now()
    return render_template('user/account.html', title='Account', form=form, user=user, post=post, users=users)


@bp.route('/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.created_at.desc()).\
        paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    return render_template('post/user_posts.html', title='User posts', posts=posts, user=user)




