from vu_sports.app.models.Team import Team
from vu_sports.app.models.User import User
from vu_sports.app.models.Event import Event, Event_Registration
from vu_sports.utils import db


class TeamRepository:
    @staticmethod
    def get_team_by_id(team_id: int):

        return db.session.query(Team).filter_by(id=team_id).first()

    @staticmethod
    def get_all_teams():

        return db.session.query(Team).all()

    @staticmethod
    def get_team_by_name(name: str):
        
        return db.session.query(Team).filter_by(name=name).first()


    @staticmethod
    def create_team(name: str, capacity: int):

        new_team = Team(name=name,capacity=capacity)
        db.session.add(new_team)
        db.session.commit()
        return new_team


    @staticmethod
    def get_registered_members(event_id: int):
        event = Event.query.get(event_id)

        members = User.query.join(Event_Registration).filter(Event_Registration.event_id == event_id,
                                                            User.sports.any(id=event.sport_id)).all()
        return members
    
    
    @staticmethod
    def get_team_members(team_id:int):
        team = db.session.query(Team).filter(Team.id == team_id).first()
        
        return team.users if team else []