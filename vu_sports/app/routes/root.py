from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import session
from vu_sports.app.models.User import User
from vu_sports.app.models.Event import Event
from vu_sports.app.models.Team import Team
from vu_sports.app.models.Sport import Sport

bp = Blueprint("root", __name__)



@bp.route("/")
def public_view():
    return render_template("public_view.html")


@bp.route('/dashboard')
@login_required
def dashboard():
    total_users = User.query.count()
    total_events = Event.query.count()
    total_teams = Team.query.count()
    total_sports = Sport.query.count()
    return render_template("dashboard.html",total_users=total_users, total_events=total_events, total_teams=total_teams, total_sports=total_sports)