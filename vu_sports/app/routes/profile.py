from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from vu_sports.utils import db
from vu_sports.app.forms.Profile import CoachProfileForm, ParticipantProfileForm
from vu_sports.app.models.Profile import Profile
from vu_sports.app.repositories.Profile import ProfileRepository
from vu_sports.app.models.User import User

bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.route("/", methods=["GET", "POST"])
@bp.route("/<int:user_id>", methods=["GET", "POST"])
@login_required
def profile(user_id=None):
    coach_form = CoachProfileForm()
    participant_form = ParticipantProfileForm()

    if user_id:
        target_user = db.query.get_or_404(user_id)
    else:
        target_user = current_user

    if target_user.role.name == "Admin":
        if target_user.id == current_user.id:
            flash("Admin don't have profiles for now.", category="warning")
        else:
            flash("You do not have permission to view this profile.", category="danger")
            return redirect(url_for("root.public_view"))

    if current_user.id != target_user.id and  current_user.role.name != "Admin":
        flash('Unauthorized access to profile.', category='danger')
        return redirect(url_for('root.public_view'))

    if request.method == "POST" :
        if target_user.role.name == "Coach" and coach_form.validate_on_submit():
            ProfileRepository.add_coach_profile(target_user.id,
            coach_form.bio.data,
            coach_form.achievements.data,
            coach_form.experience_years.data,
            coach_form.specialization.data)

            flash("Profile updated successfully!", category="success")
            return redirect(url_for("profile.view_profile",user_id=target_user.id))
        
        elif target_user.role.name == "Participant" and participant_form.validate_on_submit():
            ProfileRepository.add_participant_profile(target_user.id,
            participant_form.bio.data, 
            participant_form.achievements.data, 
            participant_form.age.data, 
            participant_form.past_participation.data, 
            participant_form.skills.data)

            flash("Profile updated successfully!", category="success")
            return redirect(url_for("profile.view_profile",user_id=target_user.id)) 
        
    return render_template("profile/profile_forms.html", coach_form=coach_form, participant_form=participant_form,user =target_user )



@bp.route("/view_profile", methods=["GET"])
@bp.route("/view_profile/<int:user_id>", methods=["GET"])
@login_required
def view_profile(user_id=None):
    targeted_id = user_id if user_id else current_user.id
    if user_id and user_id != current_user.id:
        is_admin = current_user.role.name == "Admin"
        is_coach = current_user.role.name == "Coach"
        if not (is_admin or is_coach):
            flash("You do not have permission to view this profile.", "danger")
            return redirect(url_for("root.public_view"))

    profile = Profile.query.filter_by(user_id=targeted_id).first()
    if profile is None:
        if targeted_id == current_user.id:
            flash("Profile not found. Add your profile", category="danger")
            return redirect(url_for("profile.profile"))
        else:
            flash("This user has not created a profile yet.", category="warning")
            return redirect(url_for("root.dashboard"))
    return render_template("profile/all_profiles.html", profile=profile)
    


@bp.route("/edit_profile", methods=["GET", "POST"])
@bp.route("/edit_profile/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_profile(user_id=None):
    targeted_id = user_id if user_id else current_user.id
    profile = Profile.query.filter_by(user_id=targeted_id).first()
    if not profile:
        flash("Profile not found.", category="danger")
        return redirect(url_for("profile.profile"))

    if targeted_id != current_user.id and not current_user.role.name == "Admin":
        flash("Profile not found.", category="danger")
        return redirect(url_for("root.public_view"))

    coach_form = CoachProfileForm(obj=profile)
    participant_form = ParticipantProfileForm(obj=profile)

    if request.method == "POST":
        profile_owner_role = profile.user.role.name
        
        if profile_owner_role == "Coach" and coach_form.validate_on_submit():
            ProfileRepository.edit_coach_profile(profile.id,
            coach_form.bio.data,
            coach_form.achievements.data,
            coach_form.experience_years.data,
            coach_form.specialization.data)

            flash("Profile updated successfully!", category="success")
            return redirect(url_for("profile.view_profile",user_id=profile.user_id))
        
        elif profile_owner_role == "Participant" and participant_form.validate_on_submit():
            ProfileRepository.edit_participant_profile(profile.id,
            participant_form.bio.data, 
            participant_form.achievements.data, 
            participant_form.age.data, 
            participant_form.past_participation.data, 
            participant_form.skills.data)

            flash("Profile updated successfully!", category="success")
            return redirect(url_for("profile.view_profile")) 
        
    return render_template("profile/profile_forms.html", coach_form=coach_form, participant_form=participant_form, profile=profile,user = profile.user)