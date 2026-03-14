from flask_login import UserMixin
from sqlalchemy import func
from vu_sports.app.models.Team import user_team
from vu_sports.app.models.Sport import sport_participation
from vu_sports.utils import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Foreign keys
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    role = db.relationship("Role", backref="users")
    teams = db.relationship("Team", secondary=user_team, backref="users")
    sports = db.relationship(
        "Sport", secondary=sport_participation, backref="participants"
    )
    requests = db.relationship("Request", backref="user")
