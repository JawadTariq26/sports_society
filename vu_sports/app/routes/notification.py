from flask import Blueprint, redirect, render_template, request, flash, url_for
from vu_sports.app.models.Notification import Notification
from vu_sports.app.forms.Notification import Notification_Form
from vu_sports.app.repositories.Notification import NotificationRepository
from flask_login import current_user, login_required
from vu_sports.utils import admin_required

bp = Blueprint("notification",__name__,url_prefix="/notifications" )


@bp.route("/create_notification",methods=['GET','POST'])
@login_required
@admin_required
def create_notification():
    form = Notification_Form()

    if form.validate_on_submit() and request.method == 'POST':
        NotificationRepository.create_notification(title=form.title.data, message=form.message.data, sender_id=current_user.id )
        flash('Notification Created Successfully', category='success')
        return redirect(url_for('root.dashboard'))
    return render_template('notification/send_notification.html',form= form )

    


@bp.route('/view_notification',methods=['GET'])
@login_required
def view_notification():
    all_notification = NotificationRepository.get_all_notifications()
    return render_template('notification/view_notification.html', notifications = all_notification)



@bp.route('/notification_message_pg',methods=['GET','POST'])
@login_required
@admin_required
def notification_message_pg():
    return render_template('notification/notification_message.html')