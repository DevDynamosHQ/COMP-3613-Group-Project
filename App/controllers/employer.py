from App.models import Employer
from App.database import db


def get_employer(employer_id):
    return db.session.get(Employer, employer_id)


def get_all_employers():
    return db.session.scalars(db.select(Employer)).all()



def get_all_employers_json():
    employers = get_all_employers()
    return [e.get_json() for e in employers] if employers else []


def update_employer(employer_id, company_name=None, email=None, phone=None):
    employer = get_employer(employer_id)
    if not employer:
        return False
    
    if company_name is not None:
        employer.company_name = company_name
    if email is not None:
        employer.email = email
    if phone is not None:
        employer.phone = phone
    
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

    db.session.delete(employer)
    db.session.commit()
    return True
