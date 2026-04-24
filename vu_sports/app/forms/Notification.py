from flask_wtf import FlaskForm
from wtforms import  SubmitField, StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length

class Notification_Form(FlaskForm):
    title = StringField("Title", validators=[Length(max=145)], render_kw={"placeholder": "create title here"})
    message = TextAreaField("Message", validators=[DataRequired()], render_kw={'placeholder': 'type message here'})
    submit = SubmitField("Send")


