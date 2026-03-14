from vu_sports.app.models.Role import Role
from vu_sports.utils import db


class RoleRepository:
    @staticmethod
    def get_all_roles():

        return db.session.query(Role).all()

    @staticmethod
    def get_role_by_name(name: str):

        return db.session.query(Role).filter_by(name=name).first()

    @staticmethod
    def get_role_by_id(role_id: int):

        return db.session.query(Role).filter_by(id=role_id).first()