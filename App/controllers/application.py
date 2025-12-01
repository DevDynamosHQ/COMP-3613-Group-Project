from sqlalchemy import func
from App.models import Application, Student, Position, Staff, User, Employer
from App.database import db


def create_application(student_id, position_id):
    student = db.session.get(Student, student_id)
    position = db.session.get(Position, position_id)
    
    if not student or not position:
        return None 
    existing = db.session.query(Application).filter_by(
        student_id=student.id,
        position_id=position.id
    ).first()
    if existing:
        return existing 
    
    application = Application(student_id=student.id, position_id=position.id)
    db.session.add(application)
    try:
        db.session.commit()
        return application
    except Exception as e:
        db.session.rollback()
        print(f"Error creating application: {e}")
        return None

def get_application(application_id):
    return db.session.get(Application, application_id)

def get_all_applications():
    return db.session.query(Application).all()


def get_applications_by_student(student_id):
    return db.session.query(Application).filter_by(student_id=student_id).all()

def get_applications_by_position(position_id):
    return db.session.query(Application).filter_by(position_id=position_id).all()

def get_applications_by_staff(staff_id):
    return db.session.query(Application).filter_by(staff_id=staff_id).all()

def get_applications_by_employer(employer_id):
    return (
        db.session.query(Application)
        .join(Position, Application.position_id == Position.id)
        .filter(Position.employer_id == employer_id)
        .all()
    )

def get_applications_by_position_and_state(position_id, state_name):
    applications = db.session.query(Application).filter(
        Application.position_id == position_id,
        func.lower(Application.state_name) == state_name.lower()
    ).all()
    
    return applications


def get_all_applications_json():
    return [app.get_json() for app in get_all_applications()]

def get_applications_by_student_json(student_id):
    return [app.get_json() for app in get_applications_by_student(student_id)]

def get_applications_by_position_json(position_id):
    return [app.get_json() for app in get_applications_by_position(position_id)]

def get_applications_by_staff_json(staff_id):
    return [app.get_json() for app in get_applications_by_staff(staff_id)]

def get_applications_by_employer_json(employer_id):
    applications = get_applications_by_employer(employer_id)
    return [app.get_json() for app in applications]


def shortlist_application(application_id, staff_id=None):
    application = get_application(application_id)
    if not application:
        return None

    if staff_id:
        staff_user = db.session.get(User, staff_id)  
    else:
        staff_user = None

    try:
        application.shortlist(user=staff_user)  
        db.session.commit()
        return application
    except Exception as e:
        db.session.rollback()
        print(f"Error shortlisting application: {e}")
        return None



def accept_application(application_id, employer_id=None):
    application = get_application(application_id)
    if not application:
        print("Application not found")
        return None

    
    employer = db.session.get(Employer, employer_id)
    if not employer:
        print("Invalid employer ID (not found in Employer table)")
        return None

    employer_user = db.session.get(User, employer_id)

    position = db.session.get(Position, application.position_id)
    if not position:
        print("Position not found")
        return None

    if position.number_of_positions <= 0:
        print("All positions for this job are already filled")
        return None
    
    if application.state_name != "shortlisted":
        print("Only shortlisted applications can be accepted") 
        return None
    
    if position.employer_id != employer_id:
        print("Employer cannot accept applications for another employer's position")
        return None

    
    if application.state_name == "accepted":
        print("Application has already been accepted")
        return None


    try:
        application.accept(user=employer_user)

        position.number_of_positions -= 1

        db.session.commit()
        return application
    except Exception as e:
        db.session.rollback()
        print(f"Error accepting application: {e}")
        return None




def reject_application(application_id, employer_id=None):
    application = get_application(application_id)
    if not application:
        print("Application not found")
        return None

  
    employer = db.session.get(Employer, employer_id)
    if not employer:
        print("Invalid employer ID (not found in Employer table)")
        return None

    employer_user = db.session.get(User, employer_id)

    try:
        application.reject(user=employer_user)
        db.session.commit()
        return application
    except Exception as e:
        db.session.rollback()
        print(f"Error rejecting application: {e}")
        return None




def update_application(application_id, position_id=None):
    application = get_application(application_id)
    if not application:
        return False
    
    if position_id:
        application.position_id = position_id

    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error updating application: {e}")
        return False
