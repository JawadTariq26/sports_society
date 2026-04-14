from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required,current_user
from vu_sports.utils import db, admin_required
from vu_sports.app.forms.Event import Create_Event
from vu_sports.app.models.Event import Event, Event_Registration
from vu_sports.app.repositories.Sport import SportRepository
from vu_sports.app.repositories.Event import EventRepository


bp = Blueprint("event", __name__, url_prefix="/events")


@bp.route("/create_event", methods=["GET", "POST"])
@login_required
@admin_required
def create_event():
    form = Create_Event()
    form.sport_id.choices = [(sport.id, sport.name) for sport in SportRepository.get_all_sports()]

    if form.validate_on_submit() and request.method == "POST":
        new_event = Event(
            title=form.title.data,                      #type: ignore
            category=form.category.data,                #type: ignore
            timedate=form.timedate.data,                #type: ignore
            venue=form.venue.data,                      #type: ignore
            capacity=form.capacity.data,                #type: ignore
            description=form.description.data,          #type: ignore    
            sport_id=form.sport_id.data,                #type: ignore
            created_by=current_user.id                  #type: ignore
        )
        db.session.add(new_event)
        db.session.commit()
        flash("Event created successfully!", category="success")
        return redirect(url_for("root.dashboard"))

    return render_template("events/create_event.html", form=form)


@bp.route("/show_all_events", methods=["GET"])
@login_required
def show_all_events():
    if current_user.role.name == "Admin":
        events = EventRepository.get_all_events()
    elif current_user.role.name == "Coach":
        sport_id = current_user.sports[0].id
        events = EventRepository.get_events_by_sport_id(sport_id)
    elif current_user.role.name == "Participant":
        filtered_events = []
        
        for sport in current_user.sports:
            sport_events = EventRepository.get_events_by_sport_id(sport.id)
            
            for event in sport_events:
                has_coach = any(reg.user.role.name == "Coach" for reg in event.registrations)       #type: ignore
                
                if has_coach:
                    filtered_events.append(event)
        events = filtered_events
    return render_template("events/show_all_events.html", events=events)



@bp.route('/register_event/<int:event_id>/<int:user_id>', methods=['GET','POST'])
@login_required
def register_event(event_id,user_id):
    event = EventRepository.get_event_by_id(event_id)
    if not event:
        flash('Event not found or been deleted', category='danger')
        return redirect(url_for("event.show_all_events"))
    existing_registration = db.session.query(Event_Registration).filter_by(event_id=event_id, user_id=user_id).first()
    if existing_registration:
        flash("You have already registered for this event.", category="warning")
        return redirect(url_for("event.show_all_events"))   

    current_registration_count = db.session.query(Event_Registration).filter_by(event_id=event_id).count()
    if current_registration_count >= event.capacity :                                       #type: ignore
        flash("Event is at full capacity. Registration closed.", category="danger")
        return redirect(url_for("event.show_all_events"))   

    try:
        event_registration = Event_Registration(event_id=event.id, user_id=user_id)         #type: ignore
        db.session.add(event_registration)
        db.session.commit()
        flash("Successfully registered for the event!", category="success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while registering for the event. Please try again.", category="danger")
    return redirect(url_for("event.show_all_events"))


@bp.route('/delete_event/<int:event_id>', methods=['GET','POST'])
@login_required
@admin_required
def delete_event(event_id):
    return 'pass'


@bp.route('/my_events', methods=['POST','GET'])
@login_required
def my_events():
    user_events = current_user.registrations
    
    return render_template("events/view_my_events.html", registrations=user_events)