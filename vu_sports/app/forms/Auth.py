from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, EmailField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Regexp


class RegistrationForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired(), Length(min=5, max=100)],
        render_kw={"placeholder": "Email Address"},
    )
    name = StringField(
        "Name",
        validators=[DataRequired(), Length(min=2, max=100),
        Regexp(r'^[a-zA-Z\s]+$',
        message="Name must contain only letters and spaces.")],
        render_kw={"placeholder": "Full Name"},
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)],
        render_kw={"placeholder": "Password"},
    )
    role = SelectField(
        "Role",
        validators=[DataRequired()],
        choices=[],
    )
    sports = SelectMultipleField(
        "Sport",
        validators=[DataRequired()],
        choices=[], coerce=int,
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired(), Length(min=5, max=100)],
        render_kw={"placeholder": "Email Address"},
    )
    password = PasswordField(
        "Password", validators=[DataRequired()], render_kw={"placeholder": "Password"}
    )
    submit = SubmitField("Login")
