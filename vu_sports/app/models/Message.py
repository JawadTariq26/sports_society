from vu_sports.utils import db

class Message(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text, nullable= False )
    timestamp = db.Column(db.DateTime, default = db.func.now())

    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    
    sender = db.relationship(
        "User",
        foreign_keys=[sender_id],
        backref="sent_messages"
    )

    receiver = db.relationship(
        "User",
        foreign_keys=[receiver_id],
        backref="received_messages"
    )