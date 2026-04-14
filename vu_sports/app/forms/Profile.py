from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class CoachProfileForm(FlaskForm):
    bio = StringField("Bio", validators=[Length(max=500)], render_kw={"placeholder": "Tell us about yourself"})
    achievements = StringField("Achievements", validators=[Length(max=500)], render_kw={"placeholder": "List your achievements"})
    experience_years = IntegerField("Years of Experience", validators=[DataRequired()])
    specialization = StringField("Specialization", validators=[Length(max=100)], render_kw={"placeholder": "Your coaching specialization"})
    submit = SubmitField("Submit")

class ParticipantProfileForm(FlaskForm):
    bio = StringField("Bio", validators=[Length(max=500)], render_kw={"placeholder": "Tell us about yourself"})
    achievements = StringField("Achievements", validators=[Length(max=500)], render_kw={"placeholder": "List your achievements"})
    skills = StringField("Skills", validators=[Length(max=500)], render_kw={"placeholder": "List your skills"})
    past_participation = StringField("Past Participation", validators=[Length(max=500)], render_kw={"placeholder": "List your past event participation"})
    age = IntegerField("Age", validators=[DataRequired()])
    submit = SubmitField("Submit")
    