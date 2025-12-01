from sqlalchemy import func
from App.controllers.employer import get_employer
from App.controllers.staff import get_staff
from App.models import Application, Student, Position, Staff, User, Employer
from App.database import db


def create_application(student_id, position_id):
    student = db.session.get(Student, student_id)
    position = db.session.get(Position, position_id)
    
    if not student or not position:
        return None 
    
    existing = db.session.query(Application).filter_by(student_id=student.id, position_id=position.id).first()
    
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


def shortlist_application(application_id, staff_id=None):
    application = get_application(application_id)
    if not application:
        return None

    if staff_id:
        staff_user = get_staff(staff_id)
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



def accept_application(application_id, employer_id):
    application = get_application(application_id)

    if not application:
        print("Application not found")
        return None
    
    employer = get_employer(employer_id)

    if not employer:
        print("Employer not found")
        return None

    if application.position.employer_id != employer_id:
        print("Employer cannot accept applications for another employer's position")
        return None
    
    if not application.state.can_accept():
        print("Application is not in a state that can be accepted")
        return None
    
    if application.position.number_of_positions <= 0:
        print("All positions for this job are already filled")
        return None


    try:
        application.accept(user=employer)
        application.position.number_of_positions -= 1
        db.session.commit()
        return application
    
    except Exception as e:
        db.session.rollback()
        print(f"Error accepting application: {e}")
        return None




def reject_application(application_id, employer_id):
    application = get_application(application_id)
    employer = get_employer(employer_id)

    if not application:
        print("Application not found")
        return None

  
    if not employer:
        print("Employer not found")
        return None


    try:
        application.reject(user=employer)
        db.session.commit()
        return application
    
    except Exception as e:
        db.session.rollback()
        print(f"Error rejecting application: {e}")
        return None


def delete_application(application_id):
    application = get_application(application_id)
    
    if not application:
        return None

    db.session.delete(application)
    db.session.commit()
    return True