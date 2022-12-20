from datetime import datetime

from flask import redirect, url_for, flash, request, render_template, current_app
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message
from werkzeug.urls import url_parse

from app import db, mail
from app.users import bp
from app.users.forms import LoginForm, RegisterForm, EditAccountForm, ResetRequestForm, ResetPasswordForm
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
            return redirect(url_for('users.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next_page')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('users.account')
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
        return redirect(url_for('users.login'))
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
        return redirect(url_for('users.account'))
    current_user.last_seen = datetime.now()
    return render_template('user/account.html', title='Account', form=form, user=user, post=post, users=users)


@bp.route('/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.created_at.desc()).\
        paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    return render_template('post/user_posts.html', title='User posts', posts=posts, user=user)


@bp.route('/request_user_password', methods=['GET', 'POST'])
def request_user_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('from Microblog')
        return redirect(url_for('users.login'))
    return render_template('user/reset_request.html', title='Reset password', form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    message = Message('Request a new password', sender='noreply@demo.com', recipients=[user.email])
    message_text = f"""You have requested a new password for your account:
                        {url_for('users.reset_token', token=token, _external=True)}
                        If you didn't do request, just ignore this message"""
    mail.send(message)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.varify_reset_token(token)
    if user is None:
        flash('Bed token')
        return redirect(url_for('users.request_user_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('users.login'))
    return render_template('user/reset_password.html', form=form)