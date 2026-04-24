from vu_sports.utils import db
from vu_sports.app.models.Notification import Notification



class NotificationRepository():

    @staticmethod
    def create_notification( title, message,sender_id ):
        create_notification = Notification(
            title = title,                              #type:ignore
            message = message,                          #type:ignore
            sender_id = sender_id                       #type:ignore
        )
        db.session.add(create_notification)
        db.session.commit()

    
    @staticmethod
    def get_all_notifications():
        all_notification  = db.session.query(Notification).all()
        return all_notification