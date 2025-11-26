from App.models import User, Student, Employer, Staff
from App.database import db

#edited

def create_user(username, password, user_type, email= None):
    try:
        if user_type == "student":
            new_user = Student(username=username, password=password, email=email)
        elif user_type == "employer":
            new_user = Employer(username=username, password=password, email=email)
        elif user_type == "staff":
            new_user = Staff(username=username, password=password, email=email)
        else:
            return False

        db.session.add(new_user)
        db.session.commit()
        return new_user

    except Exception as e:
        db.session.rollback()
        return False

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    return [u.get_json() for u in get_all_users()]

def update_user(id, username=None, password=None):
    user = get_user(id)
    if not user:
        return None
    
    if username:
        user.username = username
    if password:
        user.set_password(password)

    db.session.commit()
    return user
