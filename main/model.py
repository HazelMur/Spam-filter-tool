from datetime import datetime #datetime is the module and the attribute you are using of the module is also called datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from main import db, login_manager, app
from flask_login import UserMixin 
from flask_sqlalchemy import SQLAlchemy


#login extension
@login_manager.user_loader #specifies decarater
def load_user(user_id):
	return User.query.get(int(user_id)) #gets the user with that id

#Each class has its own table in the database

#User table - all registered users stored here
class User(db.Model, UserMixin): #inherting from db.Model and UserMixin
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False) 
	password = db.Column(db.String(60), nullable=False) 
	posts = db.relationship('Post', backref='author', lazy='dynamic') #Post attribute has a relationship to the POST model (lazy load the data in one go)
	is_admin = db.Column(db.Boolean, default=False)

#Post table - all sent emails stored here from the flask app
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #relationship here we are ref the table name and column name

	def __repr__(self):
		return f"Post('{self.title}', {self.date_posted}')"

#Email table - all sent emails stored here from the thunderbird and each email has a spam score
class Email(db.Model):
	id = db.Column(db.String(255), primary_key=True)
	to =  db.Column(db.String(100), nullable=False)
	sender =  db.Column(db.String(100), nullable=False)
	subject =  db.Column(db.String(300), nullable=False)
	body =  db.Column(db.String(8000), nullable=False)
	date_sent =  db.Column(db.DateTime, nullable=False)
	naive_bayes_spam =  db.Column(db.Boolean, default=False)
	svm_spam = db.Column(db.Boolean, default=False)
	random_forest_spam = db.Column(db.Boolean, default=False)
	logistic_regression_spam = db.Column(db.Boolean, default=False)


	def __repr__(self):
		return f"Email('{self.to}', {self.sender}', '{self.subject}', '{self.body}', '{self.date_sent}')"