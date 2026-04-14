from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired

class Create_Event(FlaskForm):
    title = StringField("Event Title", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    timedate = StringField("Date & Time", validators=[DataRequired()])
    venue = StringField("Venue", validators=[DataRequired()])
    capacity = IntegerField("Capacity", validators=[DataRequired()])
    description =  StringField("Description")
    sport_id = SelectField("Sport", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Create Event")