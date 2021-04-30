from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from main.model import User


# Registration Form
class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) 
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	#Create a customize validation for the register form for username
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first() #this filters to see if the username is already in the database
		if user:
			raise ValidationError('That username is taken. Please choose a different username')

	#Create a customize validation for the register form for email
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose a different email')

#Login Form
class LoginForm(FlaskForm): 
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


#Account Form
class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])

	#Create a customize validation for the register form for username
	def validate_username(self, username):
		if username.data != current_user.username: #only want to do these validate checks if the username or email is different to their previous ones
			user = User.query.filter_by(username=username.data).first() #this filters to see if the username is already in the database
			if user:
				raise ValidationError('That username is taken. Please choose a different username')

	#Create a custime validation for the register form for email
	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken. Please choose a different email')

#Form for when they first go to reset their password
class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None: #check if email doesnt exist
			raise ValidationError('There is no account with this email. You must register first.')

#Form when they do reset their password
class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')

#Email Form
class PostForm(FlaskForm):
	to = StringField('To', validators=[DataRequired()])
	title = StringField('Email Subject', validators=[DataRequired()])
	content = TextAreaField('Email Content', validators=[DataRequired()])
	submit = SubmitField('Send')