from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from main import db, bcrypt
from main.model import User, Post
from main.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, PostForm
#from main.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__) #create blueprint

#Register route
@users.route("/register", methods=['GET', 'POST']) #adding methods to allow for POST request
def register():
	if current_user.is_authenticated: #if current user is logged in redirect them to the home page
		return redirect(url_for('main1.home'))
	form = RegistrationForm()
	#Check if the data entered is validate for the form
	if form.validate_on_submit():#CHECKING IF FORM IS VALIDATE ON SUBMIT
		#Hash Password
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password) #creates a new user
		db.session.add(user) #add this user to the changes in our db
		db.session.commit() #commit these changes this will add the user to the database
		flash('Your account has now been created! You are now able to log in', 'success') #flash one time alert message, f string is used as we are passing in a variable
		#redirect to the home page after a successful creation
		return redirect(url_for('users.login')) #login is the name of the function of the route, user is returned to login page
	return render_template('register.html', title='Register', form=form)


#Login route
@users.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated: #if current user is logged in redirect them to the home page
		return redirect(url_for('main1.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first() #this will filter the emails entered into the form to see if this email exist already in the db and if it does exist returnt he first user with this email
		if user and bcrypt.check_password_hash(user.password, form.password.data): #this will check the hash password with the password they enter into the form
			login_user(user, remember=form.remember.data) #this will login the user
			next_page = request.args.get('next') #get next parameter from url if user exists (get method)
			return redirect(next_page) if next_page else redirect(url_for('main1.welcome')) #redirect to the next page if the next page exists if it is null of false return the redirect to home page
		else:
			flash('Login unsuccessful. Please check email and password', 'danger') #danger will display a red alert
	return render_template('login.html', title='Login', form=form) #return login page


#Logout route
@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('main1.home'))


#Account route
#This is used if a user clicks on a certain link and they need to be logged in order to view this data
@users.route("/account", methods=['GET', 'POST']) #allowing GET and POST requests
@login_required #this means we need to be logged in to access the account route
def account():
	form = UpdateAccountForm()
	#if form.validate_on_submit(): #validate form
		#if form.picture.data: #check for picture data
			#set users profile pic (create new function for this above in the code)
		#	picture_file = save_picture(form.picture.data)
		#	current_user.image_file = picture_file
		#current_user.username = form.username.data #we can update our username and email
		#current_user.email = form.email.data
		#db.session.commit()
		#flash('Your account has been updated!', 'success')
		#return redirect(url_for('users.account'))
	if request.method == 'GET': #populate form when user visits account page
		form.username.data = current_user.username
		form.email.data = current_user.email
		#form.password.data = current_user.password 
	#image_file = url_for('static', filename='profile_pics/' + current_user.image_file) #set imagefile to static dir
	return render_template('account.html', title='Account', form=form) #image_file=image_file


#User Posts route
#@users.route("/user/<string:username>")
#def user_posts(username):
#	page = request.args.get('page', 1, type=int)
#	user = User.query.filter_by(username=username).first_or_404() #get the first user with this username
#	posts = Post.query.filter_by(author=user)\
		#.order_by(Post.date_posted.desc())\
		#.paginate(page=page, per_page=3) #orders the posts in a specfic order and shows 5 per page
#	return render_template('user_posts.html', posts=posts, user=user)

#Route Request to reset password
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated: #make sure user is logged out before resetting password
		return redirect(url_for('main1.home'))
	form = RequestResetForm()
	if form.validate_on_submit(): #they have no submitted an email into the form
		user = User.query.filter_by(email=form.email.data).first() #get user for that email
		send_reset_email(user) #send email to the user
		flash('An email has been sent with instructions to reset your password.', 'info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Reset Password', form=form)


#Reset their password actually
#@users.route("/reset_password/<token>", methods=['GET', 'POST'])
#ef reset_token(token): #verify token from URL using the user method created
#	if current_user.is_authenticated: #make sure user is logged out before resetting password
#		return redirect(url_for('main1.home'))
#	user = User.verify_reset_token(token) 
#	if user is None:
#		flash('That is an invalid or expired token', 'warning')
#		return redirect(url_for('users.reset_request'))
#	form = ResetPasswordForm()
#	if form.validate_on_submit():#CHECKING IF FORM IS VALIDATE ON SUBMIT
#		#Hash Password
#		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#		user.password = hashed_password #hashing the users password from form.password.data
#		db.session.commit() #commit these changes to the users password
#		flash('Your password has been updated! You are now able to log in', 'success') #flash one time alert message, f string is used as we are passing in a variable
#		#redirect to the home page after a successful creation
#		return redirect(url_for('users.login'))
#	return render_template('reset_token.html', title='Reset Password', form=form)
