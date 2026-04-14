from vu_sports.app.models.Request import Request
from vu_sports.app.models.User import User
from vu_sports.app.models.Sport import Sport
from vu_sports.app.models.Role import Role
from vu_sports.app.models.Event import Event_Registration
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


    # @staticmethod
    # def update_request_status(request_id: int, new_status: str):

    #     req = db.session.query(Request).filter_by(id=request_id).first()
    #     if req:
    #         req.status = new_status
            
    #         req.user.sports.append(req.sport)
    #         db.session.commit()
    #         return req
    #     return None


    @staticmethod
    def update_request_status(request_id: int, new_status: str):
        req = db.session.query(Request).filter_by(id=request_id).first()
        if not req:
            return None, "Request not found"

        if new_status == "approved" and req.role.name == "Coach":
            existing_coach = User.query.join(Request).filter(
            User.id != req.user_id,          
            Request.sport_id == req.sport_id, 
            Request.status == "approved",     
            Request.role_id == req.role_id    
        ).first()
            if existing_coach:
                return  f"Coach {existing_coach.name.title()} is already assigned to {req.sport.name.title()}. Please Block or handle the conflict."
                
            req.status = new_status
            if req.sport not in req.user.sports:
                req.user.sports.append(req.sport)
            db.session.commit()
            return None

        elif new_status == "approved" and req.role.name == "Participant":
            req.status = new_status
            if req.sport not in req.user.sports:
                req.user.sports.append(req.sport)
            db.session.commit()
            return None

        else:
            # For rejection or other statuses, simply kardia update status
            req.status = new_status
            if req.sport in req.user.sports:
                req.user.sports.remove(req.sport)
            db.session.query(Event_Registration).filter_by(user_id = req.user_id).delete()

        db.session.commit()
        return None
    
    @staticmethod
    def get_current_user_status(user_id: int):
        req = db.session.query(Request).filter_by(user_id=user_id).all()
        if req:
            approved = list(filter(lambda r: r.status == "approved", req))
            if approved:
                return True
        return False
    
    
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
