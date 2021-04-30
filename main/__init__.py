#This file we initlize our packages and bring components together
import os 
from flask import Flask, session 
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager 
from flask_mail import Mail #how our app knows to send mail 
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import email
import mailparser


app = Flask(__name__)
app.config['SECRET_KEY'] = '35f6d593ea98517a248e1e14f958b2f6' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hazel9@127.0.0.1/pythonlogin'  #setting up database 
db = SQLAlchemy(app) #database
migrate = Migrate(app, db)


bcrypt = Bcrypt(app) #Initalize the class 
login_manager = LoginManager(app) #Initalize the class 
login_manager.login_view = 'users.login' #passing in the function name of our route
login_manager.login_message_category = 'info' #info class


mail = Mail(app) #Including the extensions
from main.users.routes import users
from main.posts.routes import posts
from main.main1.routes import main1
from main.errors.handlers import errors

app.register_blueprint(users)#register the blueprint
app.register_blueprint(posts)#register the blueprint
app.register_blueprint(main1)#register the blueprint
app.register_blueprint(errors)#register the blueprint


from main.model import Email
#this file allows me to import the scoring functions created 
from .spam_scorer import score_svm, score_nb, score_lr, score_rf

rootdir = 'C:\Program Files (x86)\hMailServer\Data'

def scrape():
	# queries email table to get all ids from the email table, the ids are the file names i the data folder
    emails = db.session.query(Email.id).all()
    # this ends the connection with the sql database
    db.session.commit()
    # this puts all of the query data into a list, so essentially puts all the file names in list
    emails = [value for (value,) in emails]
    # this is a for loop which, walks through all of the directories and sub directories of the rootdir variable above
    for subdir, dirs, files in os.walk(rootdir):
        # for each file in all of the files it is walking through
        for file in files:
        	#if the file is not in the list of emails that we made above then do the following
         if file not in emails:
         	# if the file name ends with eml do the following
          if str.lower(file[-3:])=="eml":
          	# adds the full filepath to the a variable called file_path
          	file_path = os.path.join(subdir,file)
          	# gets the mail from the file_path, parses and puts it into a variable
          	mail = mailparser.parse_from_file(file_path)
          	# just gets each of the values we need and adds to variables
          	to = mail.to[0][1]
          	from_ = mail.from_[0][1]
          	body = mail.body
          	body = body.strip()
          	subject = mail.subject
          	date = mail.date
          	file = str(file)
          	email_text = subject + ' ' + body
          	email_text = str(email_text)
          	email_text = [email_text]

            #here the scoring function created is being used
          	svm_score = score_svm(email_text)
          	svm_score = svm_score[0]
          	if svm_score == 'ham':
          		svm_score = 0
          	else:
          		svm_score = 1

          	nb_score = score_nb(email_text)
          	nb_score = nb_score[0]
          	if nb_score == 'ham':
          		nb_score = 0
          	else:
          		nb_score = 1

          	lr_score = score_lr(email_text)
          	lr_score = lr_score[0]
          	if lr_score == 'ham':
          		lr_score = 0
          	else:
          		lr_score = 1

          	rf_score = score_rf(email_text)
          	rf_score = rf_score[0]
          	if rf_score == 'ham':
          		rf_score = 0
          	else:
          		rf_score = 1

          	# adds all of them to an email object, adds that to the database session
          	db.session.add(Email(id=file,to=to,sender=from_,subject=subject,body=body,date_sent=date,naive_bayes_spam=nb_score,svm_spam=svm_score,random_forest_spam=rf_score,logistic_regression_spam=lr_score))
          	#db.session.commit()
          	# adds the file name added to the database, to the list of emails so that when we go to the next file it uses the up to date list
          	emails.append(file)
         db.session.commit()

# this is a background scheduler to schedule tasks, we use this to call the scrape function above which constantly adds new emails to the the email table from the mail server
sched = BackgroundScheduler(daemon=True)
sched.add_job(scrape,'interval',seconds=15)
sched.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: sched.shutdown()) 