from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from vu_sports.utils import admin_required, db
from vu_sports.app.forms.Sport import CreateSportForm
from vu_sports.app.repositories.Sport import SportRepository


bp = Blueprint("sport", __name__, url_prefix="/sports")


@bp.route("/")
@login_required
def list_sports():
    sports = SportRepository.get_all_sports()
    return render_template("sports/list.html", sports=sports, user=current_user)


@bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create_sport():
    form = CreateSportForm()

    if request.method == "POST":
        if form.validate_on_submit():
            SportRepository.create_sport(name=form.name.data)           #type: ignore
            flash("Sport created successfully!", category="success")
            return redirect(url_for("sport.list_sports"))

    return render_template("sports/create.html", form=form, user=current_user)


@bp.route("/<int:sport_id>")
@login_required
def edit_sport(sport_id):
    sport = SportRepository.get_sport_by_id(sport_id)
    if not sport:
        flash("Sport not found.", category="danger")
        return redirect(url_for("sport.list_sports"))

    return render_template("sports/edit.html", sport=sport, user=current_user)


@bp.route("/<int:sport_id>/delete", methods=["DELETE"])
@login_required
def delete_sport(sport_id):
    sport = SportRepository.get_sport_by_id(sport_id)
    if not sport:
        flash("Sport not found.", category="danger")
    else:
        db.session.delete(sport)
        db.session.commit()
        flash("Sport deleted successfully!", category="success")

    return redirect(url_for("sport.list_sports"))
