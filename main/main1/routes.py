from flask import render_template, request, Blueprint
from flask_login import current_user, login_required
from main.model import Post, Email, User
import datetime
from sqlalchemy import func

import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

main1 = Blueprint('main1', __name__) #create blueprint

#Home route
@main1.route("/")
@main1.route("/home")
def home():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3) #orders the posts in a specfic order and shows 5 per page
	return render_template('home.html', posts=posts)

#About route
@main1.route("/about")
def about():
	return render_template('about.html', title='About')

#Welcome route
@main1.route("/welcome")
def welcome():
	return render_template('welcome.html', title='Welcome')

#Inbox route
@main1.route("/inbox_mail")
def inbox_mail():
	email_address = current_user.email
	query_set = Email.query.filter(Email.naive_bayes_spam != 1).filter(Email.to==email_address).order_by(Email.date_sent.desc()).all()
	for email in query_set:
		print(email.date_sent)
		print(email.sender)
		print(email.subject)
		print(email.body)
	return render_template('inbox_mail.html', title='Inbox Mail', query_set=query_set) 

#Sent route
@main1.route("/sent")
def sent():
	email_address = current_user.email
	query_set = Email.query.filter(Email.naive_bayes_spam != 1 and Email.sender==email_address).order_by(Email.date_sent.desc()).all()
	for email in query_set:
		print(email.date_sent)
		print(email.to)
		print(email.subject)
		print(email.body)
	return render_template('sent.html', title='Sent Mail', query_set=query_set)

#SpamReport route
@main1.route("/spam_report")
def spam_report():

	#Report 1
	today = datetime.date.today()
	seven_days_ago = today - datetime.timedelta(days=7)
	print(seven_days_ago)
	query_set = Email.query.filter(Email.naive_bayes_spam == 1).filter(Email.date_sent > seven_days_ago).count()
	print(query_set)

	#Report 2
	spam_by_account = Email.query.with_entities(Email.to, func.count(Email.id).label('count')).filter(Email.naive_bayes_spam == 1).group_by(Email.to).all()
	print(spam_by_account)

	#Report 3
	today = datetime.date.today()
	two_days_ago = today - datetime.timedelta(days=2)
	spam_email = Email.query.filter(Email.naive_bayes_spam == 1).filter(Email.date_sent > two_days_ago).all()

	return render_template('spam_report.html', title='Spam Report', query_set=query_set, spam_by_account=spam_by_account, spam_email=spam_email)

#SpamMail route
@main1.route("/spam_mail")
def spam_mail():
	email_address = current_user.email
	query_set = Email.query.filter(Email.to == email_address).filter(Email.naive_bayes_spam == 1).order_by(Email.date_sent.desc()).all()
	for email in query_set:
		print(email.date_sent)
		print(email.sender)
		print(email.subject)
		print(email.body)
		print(email.naive_bayes_spam)
	return render_template('spam_mail.html', title='Spam Mail', query_set=query_set)

#Registered_users route
@main1.route("/registered_users")
def registered_users():
	user_set = User.query.all() #this line outputs the first 3 columns in the USERS table
	print(user_set)

	return render_template('registered_users.html', title='Registered Users', user_set=user_set)

#Report 2 graph
@main1.route("/plot.png")
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	email = Email.query.with_entities(Email.to).filter(Email.naive_bayes_spam == 1).group_by(Email.to).all()
	email_result = [r for r, in email]
	count = Email.query.with_entities(func.count(Email.id).label('count')).filter(Email.naive_bayes_spam == 1).group_by(Email.to).all()
	count_result = [r for r, in count]
	axis.bar(email_result, count_result)
	return fig


