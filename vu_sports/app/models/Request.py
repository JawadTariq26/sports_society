from sqlalchemy import func
from vu_sports.utils import db


class Request(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    sport_id = db.Column(db.Integer, db.ForeignKey("sports.id"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    status = db.Column(db.String(20), default="pending")

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    sport = db.relationship("Sport", backref="requests", lazy='joined')
    role = db.relationship("Role", backref="requests", lazy='joined')
