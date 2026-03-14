from vu_sports.app.models.User import User
from vu_sports.utils import db


class UserRepository:
    @staticmethod
    def get_by_id(user_id: int):

        return db.session.query(User).get(user_id)

    @staticmethod
    def get_by_email(email: str):

        return db.session.query(User).filter_by(email=email).first()

    @staticmethod
    def create_user(name: str, email: str, password: str, role_id: int):

        new_user = User(
            name=name,
            email=email,
            password_hash=password,
            role_id=role_id,
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user
