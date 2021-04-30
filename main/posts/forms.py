from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

#Compose Mail form 
class PostForm(FlaskForm):
	to = StringField('To', validators=[DataRequired()]) 
	title = StringField('Subject', validators=[DataRequired()])
	content = TextAreaField('Body', validators=[DataRequired()])
	submit = SubmitField('Send')
	