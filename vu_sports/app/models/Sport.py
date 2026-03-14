from sqlalchemy import func
from vu_sports.utils import db


sport_participation = db.Table(
    "sport_participation",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("sport_id", db.Integer, db.ForeignKey("sports.id"), primary_key=True),
)


class Sport(db.Model):
    __tablename__ = "sports"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
