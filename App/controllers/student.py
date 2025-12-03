from App.models import Student
from App.database import db
from datetime import date, datetime


def get_student(student_id):
    return db.session.get(Student, student_id)


def get_all_students():
    return db.session.scalars(db.select(Student)).all()


def get_all_students_json():
    students = get_all_students()
    return [s.get_json() for s in students] if students else []


def update_student(student_id, username=None, email=None, dob=None, gender=None, degree=None, phone=None, gpa=None, resume=None, profile_pic=None):
    student = get_student(student_id)

    if not student:
        return None
    
    if username is not None:
        student.username = username

    if email is not None:
        student.email = email

    if dob is not None:
        if isinstance(dob, str):
            try:
                student.dob = datetime.strptime(dob, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
                return False
        elif isinstance(dob, date):
                student.dob = dob  
        else:
            print("Invalid date type. Use a string in YYYY-MM-DD format or a date object.")
            return False

    if gender is not None:
        student.gender = gender

    if degree is not None:
        student.degree = degree

    if phone is not None:
        student.phone = phone

    if gpa is not None:
        student.gpa = gpa

    if resume is not None:
        student.resume = resume

    if profile_pic is not None:
        student.profile_pic = profile_pic

    try:
        db.session.commit()
        return True
    
    except Exception as e:
        db.session.rollback()
        print(f"Error updating student: {e}")
        return False


def delete_student(student_id):
    student = get_student(student_id)

    if not student:
        return False

    try:
        db.session.delete(student)
        db.session.commit()
        return True
    
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting student: {e}")
        return False