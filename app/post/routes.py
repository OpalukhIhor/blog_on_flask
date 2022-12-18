from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required

from app import db
from app.models import Post
from app.post import bp
from app.post.forms import AddPostForm


@bp.route('/post/new', methods=['GET', 'POST'])
def new_post():
    form = AddPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                    category=form.category.data, author=current_user)
        db.session.add(post)

        db.session.commit()
        flash('Post added')
        return redirect(url_for('post.posts_list'))
    return render_template('post/add_post.html', title='Add Post', form=form)


@bp.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('post/post.html', title=post.title, post=post)


@bp.route('/posts_list')
def posts_list():
    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page,
                                                                 per_page=current_app.config['POSTS_PER_PAGE'],
                                                                 error_out=False)
    return render_template('post/posts_list.html', title='Posts', posts=posts)


@bp.route('/search')
def search():
    keyword = request.args.get('q')
    search_result = Post.query.msearch(keyword, fields=['title', 'content'], limit=5)
    return render_template('post/search.html', search_result=search_result)


@bp.route('/posts/<string:category>/', methods=['GET', 'POST'])
def category(category):
    current_category = Post.query.filter_by(category=category).first()
    posts_category = Post.query.filter_by(category=category).all()
    return render_template('post/posts_category_list.html',current_category=current_category,
                           posts_category=posts_category, title='Category ' + category)


