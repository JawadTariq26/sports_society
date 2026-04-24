from vu_sports.app.models.Team import Team
from vu_sports.app.models.Event import Event
from vu_sports.app.models.User import User
from vu_sports.app.repositories.Team import TeamRepository
from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify
from flask_login import login_required, current_user
from vu_sports.utils import db
from vu_sports.app.forms.Team import CreateTeamForm
from vu_sports.utils import admin_required, coach_required, coach_or_participant_required, coach_or_admin_required

bp = Blueprint("team",__name__,url_prefix="/teams")

@bp.route("/create_team/<int:event_id>", methods=['GET','POST'])
@login_required
@coach_required
def create_team(event_id):
    form = CreateTeamForm()
    team_name = form.name.data
    capacity = form.capacity.data

    get_event = Event.query.get(event_id)
    if get_event:
        if form.validate_on_submit() and request.method == "POST":
            if TeamRepository.get_team_by_name(team_name):                                   #type: ignore
                flash("Team name already exists. Please choose a different name.", category="danger")
            else:
                new_team = TeamRepository.create_team(name=team_name, capacity=capacity)     #type: ignore
                get_event.teams.append(new_team)
                db.session.commit()
                flash("Team created successfully!", category="success")
                return redirect(url_for("root.dashboard"))
    return render_template('teams/create_teams.html', form=form)


@bp.route("/view_teams/<int:event_id>",methods = ['GET'])
@login_required
def view_teams(event_id):
    get_event = Event.query.get(event_id)
    all_teams = get_event.teams                                                             #type: ignore
    return render_template("teams/view_teams.html", teams= all_teams)


@bp.route("/add_participant/<int:team_id>/<int:user_id>", methods=['GET','POST'])
@login_required
@coach_or_participant_required
def add_participant(team_id,user_id):
    team = Team.query.get(team_id)
    user = User.query.get(user_id)

    event = team.events[0] if team.events else None                                 #type: ignore

    if event:
        already_assigned = any(t in user.teams for t in event.teams)                #type: ignore
        if already_assigned:
            flash("User is already assigned to a team in this event.", category='danger')
            return redirect(url_for('team.registered_members',event_id=event.id))
        
    if team and user:
        if len(team.users) < team.capacity:
            team.users.append(user)
            db.session.commit()
            flash('Participant added to team successfully', category='success')
        else:
            flash('Team already full', category='danger')
    else:
        flash('SOrry', category="danger")        
    return redirect(url_for('team.registered_members', event_id=team.events[0].id))  #type: ignore


@bp.route("/remove_participant/<int:team_id>/<int:participant_id>", methods=['GET','POST'])
@login_required
@coach_or_participant_required
def remove_participant(team_id, participant_id):
    team = Team.query.get(team_id)
    particpant = User.query.get(participant_id)

    if team and particpant:
        if particpant in team.users:
            team.users.remove(particpant)
            db.session.commit()
            flash('Participant removed from team successfully', category= 'success')
        else:
            flash('Participant not in team', category='danger')
    else:
        flash('Team or participant not found', category="danger")

    return redirect(url_for('team.registered_members', event_id=team.events[0].id)) #type: ignore


@bp.route("/delete_team/<int:team_id>", methods=['GET','POST'])
@login_required
@coach_or_admin_required
def delete_team(team_id):
    get_team = Team.query.get(team_id)
    if get_team:
        get_team.users = []
        get_team.events = []
        db.session.delete(get_team)
        db.session.commit()
        flash('Team deleted successfully', category = 'success')
    return redirect(url_for('root.dashboard'))


@bp.route("/registered_members/<int:event_id>", methods=['GET','POST'])
@login_required
def registered_members(event_id):
    event = Event.query.get(event_id)
    members = TeamRepository.get_registered_members(event_id)
    avalaible_teams = event.teams                                                   #type: ignore
    return render_template("teams/registered_members.html", members=members , avalaible_teams=avalaible_teams)


@bp.route('/view_all_teams', methods=['GET'])
@login_required
@admin_required
def view_all_teams():
    teams = TeamRepository.get_all_teams()
    return render_template("teams/all_teams.html", teams=teams)


# @bp.route('/team_members',methods = ['GET','POST'])
# def team_member():
#     sorted_teams = sorted(current_user.teams, key=lambda x: x.id)
#     all_members = []
#     seen_user_ids = set() 
#     print(current_user.id)
#     for team in sorted_teams:
#         team_users = TeamRepository.get_team_members(team.id)
#         for user in team_users:
#             if user.id not in seen_user_ids:
#                 all_members.append(user)
#                 seen_user_ids.add(user.id)

#     return render_template('messages/send_message.html',members=all_members)
