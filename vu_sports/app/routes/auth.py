from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from vu_sports.app.forms.Auth import LoginForm, RegistrationForm
from vu_sports.app.repositories.Request import RequestRepository
from vu_sports.app.repositories.Role import RoleRepository
from vu_sports.app.repositories.Sport import SportRepository
from vu_sports.app.repositories.User import UserRepository
from vu_sports.utils import db
from werkzeug.security import check_password_hash, generate_password_hash
from vu_sports.app.models.User import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register() -> str:
    form = RegistrationForm()
    form.role.choices = [
        (role.id, role.name)
        for role in RoleRepository.get_all_roles()
        if role.name != "Admin"]
    form.sports.choices = [ (sport.id, sport.name) for sport in SportRepository.get_all_sports()]

    if request.method == "POST":
        if form.validate_on_submit():
            if UserRepository.get_by_email(form.email.data):                                #type: ignore
                flash("Email already registered.", category="warning")
                return render_template("auth/register.html", form=form)
            else:
                selected_sports = form.sports.data
                role = RoleRepository.get_role_by_id(form.role.data)                        #type: ignore

                if role.name == "Coach" and len(selected_sports) != 1:                      #type: ignore
                    flash("Coaches must select exactly one sport.", category="warning")
                    return render_template("auth/register.html", form=form)
                
                if role.name == "Participant" and len(selected_sports)  > 2 or len(selected_sports) == 0:   #type: ignore
                    flash("Participants can select maximum 2 sports.", category="warning")
                    return render_template("auth/register.html", form=form)

                user = UserRepository.create_user(
                    name=form.name.data,                                                    #type: ignore
                    email=form.email.data,                                                  #type: ignore
                    password=generate_password_hash(form.password.data),                    #type: ignore
                    role_id=form.role.data,
                )
                db.session.flush()

                for sport_id in selected_sports:                                           #type: ignore
                    RequestRepository.create_request(
                        user_id=user.id,
                        sport_id=sport_id,
                        role_id=form.role.data
                )
                db.session.commit()
                flash("Registration successful! Please log in.", category="success")
                return redirect(url_for("auth.login"))                                     #type: ignore

    return render_template("auth/register.html", form=form)



@bp.route("/login", methods=["GET", "POST"])
def login() -> str:
    form = LoginForm()
    # flash_messages = list()

    if request.method == "POST":
        if form.validate_on_submit():
            user = UserRepository.get_by_email(form.email.data)                     #type: ignore
            if not user:
                flash('Please Registered First To Login',category='danger')
                return redirect(url_for("auth.register"))                           #type: ignore
            approved = RequestRepository.get_current_user_status(user.id) if user else None
            current_role = user.role.name if user else None

            if user and check_password_hash(user.password_hash, form.password.data) and approved is True or current_role == 'Admin':    #type: ignore
                login_user(user)
                flash("Login successful!", category="success")
                return redirect(url_for("root.dashboard"))                           #type: ignore
        
            flash("Invalid email or password or request pending.", category="danger")

    return render_template("auth/login.html", form=form) #flash_messages=flash_messages


@bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout() -> str:
    logout_user()
    flash("You have been logged out.", category="info")
    return redirect(url_for("root.public_view"))                                      #type: ignore
