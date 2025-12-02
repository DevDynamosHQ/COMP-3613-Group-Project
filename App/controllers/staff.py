from App.models import Staff
from App.database import db


def get_staff(staff_id):
    return db.session.get(Staff, staff_id)


def get_all_staff():
    return db.session.scalars(db.select(Staff)).all()


def get_all_staff_json():
    staff = get_all_staff()
    return [s.get_json() for s in staff] if staff else []


def update_staff(staff_id, username=None, email=None):
    staff = get_staff(staff_id)

    if not staff:
        return None

    if username is not None:
        staff.username = username

    if email is not None:
        staff.email = email

    try:
        db.session.commit()
        return True
    
    except Exception as e:
        db.session.rollback()
        print(f"Error updating staff: {e}")
        return False


def delete_staff(staff_id):
    staff = get_staff(staff_id)

    if not staff:
        return None

    try:
        db.session.delete(staff)
        db.session.commit()
        return True
    
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting staff: {e}")
        return False

