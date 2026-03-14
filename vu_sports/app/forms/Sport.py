from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CreateSportForm(FlaskForm):
    name = StringField(
        "Sport Name",
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={"placeholder": "Enter sport name"},
    )
    submit = SubmitField("Create Sport")
