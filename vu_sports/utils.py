from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy.session import Session
from sqlalchemy.orm import scoped_session
from sqlalchemy import MetaData

from functools import wraps
from flask import abort
from flask_login import current_user


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
login_manager = LoginManager()
bootstrap = Bootstrap5()

# admin decorator
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != "Admin":
            abort(403) 
        return func(*args, **kwargs)
    return wrapper

# coach decorator
def coach_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != "Coach":
            abort(403) 
        return func(*args, **kwargs)
    return wrapper

def coach_or_participant_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or \
           current_user.role.name not in ["Coach", "Participant"]:
            abort(403)
        return func(*args, **kwargs)
    return wrapper

def coach_or_admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or \
           current_user.role.name not in ["Coach", "Admin"]:
            abort(403)
        return func(*args, **kwargs)
    return wrapper


def configure_login_manager():
    login_manager.login_view = "auth.login"
    login_manager.refresh_view = "auth.login"
    login_manager.login_message_category = "info"
    login_manager.login_message = "Please log in to access this page."
    login_manager.needs_refresh_message_category = "warning"
    login_manager.needs_refresh_message = (
        "Your session has expired. Please log in again."
    )

    @login_manager.user_loader
    def load_user(user_id):
        from vu_sports.app.models.User import User

        return User.query.get(int(user_id))


def get_db_session() -> scoped_session[Session]:
    """Helper function to get the current database session."""
    return db.session


def seed_db():
    from vu_sports.app.models.Role import Role
    from vu_sports.app.models.User import User
    from vu_sports.app.models.Request import Request
    from werkzeug.security import generate_password_hash

    # Seed roles
    Session = get_db_session()
    with Session() as session:
        # Seed roles
        roles = ["Admin", "Coach", "Participant"]
        for role_name in roles:
            if not session.query(Role).filter_by(name=role_name).first():
                role = Role(name=role_name)         #type: ignore
                session.add(role)
                session.flush()

        # Creating initial admin user
        admin_role = session.query(Role).filter_by(name="Admin").first()
        if (admin_role and not session.query(User).filter_by(email="admin@vu.com").first()):
            admin_user = User(
                name="Admin User",                                      #type: ignore
                email="admin@vu.com",                                   #type: ignore
                password_hash=generate_password_hash("admin123"),       #type: ignore
                role_id=admin_role.id,                                  #type: ignore
            )
            request = Request(
                user_id=admin_user.id,                                   #type: ignore
                sport_id=None,                                           #type: ignore
                role_id=admin_role.id,                                  #type: ignore
                status="approved",                                        #type: ignore
            )

            session.add(admin_user)
            session.flush()

        session.commit()
