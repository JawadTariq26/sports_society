from vu_sports.app.models.Team import Team
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
    def create_team(name: str):

        new_team = Team(name=name)
        db.session.add(new_team)
        db.session.commit()
        return new_team
