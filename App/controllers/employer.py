from App.models import Employer
from App.database import db


def get_employer(employer_id):
    return db.session.get(Employer, employer_id)


def get_all_employers():
    return db.session.scalars(db.select(Employer)).all()


def get_all_employers_json():
    employers = get_all_employers()
    return [e.get_json() for e in employers] if employers else []


def update_employer(employer_id, username=None, company=None, email=None, phone=None, profile_pic=None):
    employer = get_employer(employer_id)

    if not employer:
        return False
    
    if username is not None:
        employer.username = username
    
    if company is not None:
        employer.company = company  

    if email is not None:
        employer.email = email

    if phone is not None:
        employer.phone = phone

    if profile_pic is not None:
        employer.profile_pic = profile_pic
    
    try:
        db.session.commit()
        return True
    
    except Exception as e:
        db.session.rollback()
        print(f"Error updating employer: {e}")
        return False


def delete_employer(id):
    employer = get_employer(id)
    if not employer:
        return None

    try: 
        db.session.delete(employer)
        db.session.commit()
        return True
    
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting employer: {e}")
        return False

