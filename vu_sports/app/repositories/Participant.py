from vu_sports.utils import db
from vu_sports.app.models.User import User
from vu_sports.app.models.Sport import Sport

class ParticipantRepository:
    
    @staticmethod
    def get_total_prt_sport(sport_id: int):
        return db.session.query(User).join(Sport).filter(Sport.id == sport_id, User.role.has(name='Participant')).count()