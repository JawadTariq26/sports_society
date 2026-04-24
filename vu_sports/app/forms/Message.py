from flask_wtf import FlaskForm
from wtforms import  SubmitField, TextAreaField
from wtforms.validators import DataRequired

class MessageForm(FlaskForm):
    body = TextAreaField("Message", validators=[DataRequired()], render_kw={'placeholder': 'Type your message here'})
    Submit = SubmitField('Send')