from sqlalchemy import func
from vu_sports.utils import db



event_participation = db.Table(
    "event_participation",
    db.Column('event_id', db.Integer, db.ForeignKey("events.id"), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey("teams.id"), primary_key=True)
)

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    timedate = db.Column(db.String(50), nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    sport_id = db.Column(db.Integer, db.ForeignKey("sports.id"), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    registrations = db.relationship("Event_Registration", backref="event", lazy='joined')
    sport = db.relationship("Sport", backref="events") 




class Event_Registration(db.Model):
    __tablename__ = "event_registrations"
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    registered_at = db.Column(db.DateTime, default=func.now())
    status = db.Column(db.String(20), default="registered")


