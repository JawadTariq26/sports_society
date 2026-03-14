from vu_sports.app.repositories.Participant import ParticipantRepository
from flask import Blueprint, render_template,url_for, redirect


bp = Blueprint("participant", __name__, url_prefix="/participants")

@bp.route("/sport/<int:sport_id>")
def participants_by_sport(sport_id):
    total_participants = ParticipantRepository.get_total_prt_sport(sport_id)
    print(total_participants)
    return redirect(url_for('root.dashboard',sport_id=sport_id, total_participants=total_participants))