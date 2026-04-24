from flask import flash

from vu_sports.app.routes import event
from vu_sports.app.routes.auth import login
from vu_sports.utils import db
from vu_sports.app.models.Message import Message
from vu_sports.app.models.Event import Event, Event_Registration
from vu_sports.app.models.Team import Team
from flask_login import current_user
from vu_sports.app.repositories.Team import TeamRepository

class MessageRepository:
    
    @staticmethod
    def send_message(sender_id: int, receiver_id: int, body: str):
        new_message = Message(sender_id=sender_id, receiver_id=receiver_id, body=body) #type:ignore
        db.session.add(new_message)
        db.session.commit()
        return new_message
    


    @staticmethod
    def coach_message():
        try:
            registers = [reg.event_id for reg in current_user.registrations]
            registration = Event_Registration.query.filter_by(
            event_id=registers[0],
            user_id=current_user.id
            ).first()

            event_id = registration.event_id if registration else None        

            if event_id:
                get_all_teams = Team.query.filter(Team.events.any(id=event_id)).all()
                
                if get_all_teams:
                    get_all_members = []
                    for team in get_all_teams:
                        members = TeamRepository.get_team_members(team.id)
                        
                        get_all_members.extend(members)
                    # breakpoint()
                    return get_all_members     
                else:
                    flash("No teams found for the event.", "danger")
                    return [] 
            else:
                flash("No event found for the current user.", "danger")
                return []
        except Exception as e:
            flash('User not registered for any events. Or No teams found for the event.', 'danger')
            return []