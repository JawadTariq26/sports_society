from vu_sports.utils import db
from sqlalchemy import func

class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    
    bio = db.Column(db.Text, nullable=True)
    achievements = db.Column(db.Text, nullable=True)
    profile_pic = db.Column(db.String(255), default='default.jpg')

     
    # Coach
    experience_years = db.Column(db.Integer, nullable=True)
    specialization = db.Column(db.String(100), nullable=True)
    
    # Participant
    age = db.Column(db.Integer, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    past_participation = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())


    user = db.relationship("User", backref=db.backref("profile", uselist=False))