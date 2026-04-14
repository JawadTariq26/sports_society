from vu_sports.app.models.Sport import Sport
from vu_sports.utils import db


class SportRepository:
    @staticmethod
    def get_sport_by_id(sport_id: int):

        return db.session.query(Sport).filter_by(id=sport_id).first()

    @staticmethod
    def get_all_sports():

        return db.session.query(Sport).all()

    @staticmethod
    def get_sport_by_name(name: str):

        return db.session.query(Sport).filter_by(name=name).first()

    @staticmethod
    def create_sport(name: str):

        new_sport = Sport(name=name) 
        db.session.add(new_sport)
        db.session.commit()
        return new_sport
