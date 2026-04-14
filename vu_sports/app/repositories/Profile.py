from vu_sports.utils import db
from vu_sports.app.models.User import User
from vu_sports.app.models.Profile import Profile


class ProfileRepository:
    @staticmethod
    def add_coach_profile(user_id, bio, achievements,experience,specialization):
        new_profile = Profile(
            user_id=user_id,                    #type: ignore
            bio=bio,                            #type: ignore
            achievements=achievements,          #type: ignore
            experience_years=experience,        #type: ignore
            specialization=specialization       #type: ignore
            # later add profile picture
        )
        db.session.add(new_profile)
        db.session.commit()


    @staticmethod
    def add_participant_profile(user_id, bio, achievements, age, past_participation, skills):
        new_profile = Profile(
            user_id=user_id,                        #type: ignore
            bio=bio,                                #type: ignore
            achievements=achievements,              #type: ignore
            age=age,                                #type: ignore
            past_participation=past_participation,  #type: ignore
            skills=skills                           #type: ignore
            # later add profile picture
        )
        db.session.add(new_profile)
        db.session.commit()

    
    @staticmethod
    def edit_coach_profile(profile_id, bio, achievements,experience,specialization):
        profile = db.session.query(Profile).filter_by(id=profile_id).first()
        if profile:
            profile.bio = bio
            profile.achievements = achievements
            profile.experience_years = experience
            profile.specialization = specialization
            db.session.commit()

    @staticmethod
    def edit_participant_profile(profile_id, bio, achievements, age, past_participation, skills):
        profile = db.session.query(Profile).filter_by(id=profile_id).first()
        if profile:
            profile.bio = bio
            profile.achievements = achievements
            profile.age = age
            profile.past_participation = past_participation
            profile.skills = skills
            db.session.commit()