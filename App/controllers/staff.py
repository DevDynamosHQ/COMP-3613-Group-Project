from App.models import Staff
from App.database import db

def create_staff(username, user_id, password):
    staff = Staff(username=username,user_id = user_id, password=password)
    staff.password = password
    db.session.add(staff)
    db.session.commit()
    return staff

def get_staff(id):
    return db.session.get(Staff, id)

def get_staff_by_user(user_id):
    return db.session.execute(db.select(Staff).filter_by(user_id=user_id)).scalar_one_or_none()

def get_all_staff():
    return db.session.scalars(db.select(Staff)).all()

def get_all_staff_json():
    Staff = get_all_staff()
    return [s.get_json() for s in staff]

def update_staff(id, username):
    staff = get_staff(id)

    if not staff:
        return None

    if username is not None:
        staff.username = username

    db.session.commit()
    return staff

def delete_staff(id):
    staff = get_staff(id)
    if not staff:
        return None

    db.session.delete(staff)
    db.session.commit()
    return True
