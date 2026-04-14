from vu_sports.utils import db
from vu_sports.app.models.Event import Event, Event_Registration
from vu_sports.app.models.User import User

class EventRepository:
    @staticmethod
    def get_event_by_id(event_id: int):
        return db.session.query(Event).filter_by(id=event_id).first()

    @staticmethod
    def get_all_events():
        return db.session.query(Event).all()
    

    @staticmethod
    def get_events_by_sport_id(sport_id: int):
        return db.session.query(Event).filter_by(sport_id=sport_id).all()
    

    