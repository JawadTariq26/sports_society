from vu_sports.app.repositories.Request import RequestRepository
from flask import Blueprint, flash, redirect, render_template, request, url_for
from vu_sports.utils import admin_required, coach_required
from flask_login import login_required, current_user

bp = Blueprint("user_request", __name__, url_prefix="/requests")


@bp.route("/")
@login_required
@admin_required
def all_requests():
    requests = RequestRepository.get_all_requests()
    return render_template("requests/list.html", requests=requests)


@bp.route('/approve/<int:request_id>', methods=['GET','POST'])
@admin_required
def approve_request(request_id):
    error = RequestRepository.update_request_status(request_id, 'approved')
    if error:
        flash(error, 'danger')                                                  #type: ignore
    else:
        flash('Request approved successfully!', 'success')
    return redirect(url_for('user_request.all_requests'))


@bp.route('/block/<int:request_id>', methods=['GET','POST'])
@admin_required
def block_request(request_id):
    RequestRepository.update_request_status(request_id, 'blocked')
    flash('Request blocked successfully!', 'success')
    return redirect(url_for('user_request.all_requests'))   


# handling participant request serparate with coach access only
# @bp.route("/participants")
# @coach_required
# def prt_all_requests():
#     # requests = RequestRepository.get_all_requests()
#     # prt_request = [req for req in requests if req.role.name == 'Participant']
#     coach = current_user
#     sport_id = coach.sport[0].id if coach.sports else None

    
#     prt_request = RequestRepository.get_requests_only_prt(sport_id)
#     return render_template("requests/list.html", requests=prt_request)

@bp.route("/participants")
@coach_required
def prt_all_requests():
    coach = current_user

    sport_id = coach.sports[0].id if coach.sports else None

    prt_request = RequestRepository.get_requests_only_prt(sport_id)
    return render_template("requests/list.html", requests=prt_request)



@bp.route('/approve_prt/<int:request_id>', methods=['GET','POST'])
@coach_required
def approve_prt_request(request_id):
    RequestRepository.update_request_status(request_id, 'approved')
    flash('Request approved successfully!', 'success')
    return redirect(url_for('user_request.prt_all_requests'))



@bp.route('/block_prt/<int:request_id>', methods=['GET','POST'])
@coach_required
def block_prt_request(request_id):
    RequestRepository.update_request_status(request_id, 'blocked')
    flash('Request blocked successfully!', 'success')
    return redirect(url_for('user_request.prt_all_requests')) 