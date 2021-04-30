from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from main import db
from main.model import Post
from main.posts.forms import PostForm

posts = Blueprint('posts', __name__) #create blueprint

#Compose a new mail route
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user) #create email
		db.session.add(post) #add email to database
		db.session.commit()
		flash('Your email has been sent!', 'success')
		return redirect(url_for('main1.home'))
	return render_template('create_post.html', title='Compose Mail', form=form, legend='Compose Mail')