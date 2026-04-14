from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class CreateTeamForm(FlaskForm):
    name = StringField(
        "Team Name",
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={"placeholder": "Enter team name"},
    )
    capacity = IntegerField(
        "Team Capacity",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter team capacity"},)
    
    submit = SubmitField("Create Team")