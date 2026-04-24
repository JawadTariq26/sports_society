from ast import stmt

from flask import Blueprint, flash, render_template,url_for, redirect, request
from vu_sports.app.forms.Message import MessageForm
from vu_sports.app.models.Message import Message
from vu_sports.app.repositories.Message import MessageRepository
from flask_login import login_required, current_user
from vu_sports.app.repositories.Team import TeamRepository
from vu_sports.app.models.User import User
from vu_sports.app.models.Event import Event, Event_Registration
from vu_sports.utils import db
from vu_sports.app.models.Request import Request

bp = Blueprint("message", __name__, url_prefix="/messages")



@bp.route("/send_message", defaults={'event_id': 0}, methods=['GET','POST'])
@bp.route("/send_message/<int:event_id>", methods=['GET','POST'])
@login_required
def send_message_page(event_id):
    if event_id == 0:
        teams_to_check = current_user.teams  
    else:
        event_obj = Event.query.get(event_id)
        teams_to_check = event_obj.teams if event_obj else []

    all_entries = []
    for team in teams_to_check:
        team_users = TeamRepository.get_team_members(team.id)
        
        team_event = team.events[0] if team.events else None
        
        coach = None
        if team_event:
            for reg in team_event.registrations:
                if reg.user.role.name == "Coach":
                    coach = reg.user
                    break 
        # breakpoint()
        for user in team_users:
            all_entries.append({
                'user': user,
                'team': team,
                'event': team_event,
                'coach': coach
            })

    receiver_id = request.form.get('receiver_id', type=int) or request.args.get('message_to', type=int)
    selected_team_id = request.args.get('team_id', type=int, default=0)
    form = MessageForm()
    if form.validate_on_submit() and request.method == 'POST' and receiver_id:
        MessageRepository.send_message(sender_id=current_user.id, receiver_id=receiver_id, body=form.body.data) #type:ignore
        flash("Message sent successfully!", "success")
        return redirect(url_for('message.send_message_page', event_id=event_id))
    return render_template("messages/send_message.html",entries=all_entries, form=form, receiver_id=receiver_id,selected_team_id=selected_team_id,event_id=event_id)


@bp.route("/send_message_coach", methods=["GET", "POST"])
@bp.route("/send_message_coach/<int:receiver_id>", methods=['GET','POST'])
@login_required
def send_message_coach(receiver_id=None):
    form = MessageForm()
    if current_user.role.name == "Admin":
        stmt = db.select(User).where(User.requests.any(Request.status == 'approved'))
        members = db.session.scalars(stmt).unique().all()
    else:
        members = MessageRepository.coach_message() 

    selected_member = None
    if receiver_id:
        selected_member = User.query.get(receiver_id)

    if form.validate_on_submit() and request.method == 'POST' and receiver_id:
        MessageRepository.send_message(sender_id=current_user.id, receiver_id=receiver_id, body=form.body.data) #type:ignore
        flash("Message sent successfully!", "success")
        return redirect(url_for('root.dashboard'))
    return render_template("messages/send_message_coach.html", form=form, members=members, selected_member=selected_member)



@bp.route('/receive_message',methods= ['GET','POST'])
@login_required
def receive_message():
    messages = Message.query.filter_by(
        receiver_id=current_user.id).order_by(Message.timestamp.desc()).all()

    return render_template("messages/view_message.html",messages=messages)


@bp.route('/view_sent_message',methods= ['GET'])
@login_required
def view_sent_message():
    sent_messages = Message.query.filter_by(sender_id=current_user.id).order_by(Message.timestamp.desc()).all()
    return render_template("messages/view_sent_message.html", messages=sent_messages)

