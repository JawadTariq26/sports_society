from vu_sports.utils import db
from sqlalchemy import func

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable= False)
    message = db.Column(db.Text, nullable= False)
    created_at = db.Column(db.DateTime, default= db.func.now())

    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)

    sender = db.relationship('User')

    