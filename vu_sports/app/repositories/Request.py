from vu_sports.app.models.Request import Request
from vu_sports.app.models.Role import Role
from vu_sports.utils import db


class RequestRepository:
    @staticmethod
    def get_request_by_id(request_id: int):

        return db.session.query(Request).filter_by(id=request_id).first()

    @staticmethod
    def get_all_requests():

        return db.session.query(Request).all()
    

    
    @staticmethod
    def get_requests_only_prt( sport_id):

        query = db.session.query(Request).join(
            Role
            ).filter(
                Role.name == 'Participant'
                ).filter(
                    Request.sport_id == sport_id
                        )
        return query.all()


    @staticmethod
    def update_request_status(request_id: int, new_status: str):

        req = db.session.query(Request).filter_by(id=request_id).first()
        if req:
            req.status = new_status
            
            req.user.sports.append(req.sport)
            db.session.commit()
            return req
        return None
    
    @staticmethod
    def get_current_user_status(user_id: int):
        req = db.session.query(Request).filter_by(user_id=user_id).first()
        if req:
            return req.status
        return None
    
    @staticmethod
    def create_request(user_id: int, sport_id: int, role_id: int):

        new_request = Request(
            user_id=user_id,
            sport_id=sport_id,
            role_id=role_id
        )
        db.session.add(new_request)
        db.session.commit()
        return new_request
