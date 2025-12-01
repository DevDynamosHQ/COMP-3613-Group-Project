from App.models import Student
from App.database import db


def get_student(student_id):
    return db.session.get(Student, student_id)


def get_all_students():
    return db.session.scalars(db.select(Student)).all()


def get_all_students_json():
    students = get_all_students()
    return [s.get_json() for s in students] if students else []


def update_student(student_id, email=None, dob=None, gender=None, degree=None, phone=None, gpa=None, resume=None):
    student = get_student(student_id)

    if not student:
        return None

    if email is not None:
        student.email = email

    if dob is not None:
        student.dob = dob

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

    try:
        db.session.commit()
        return True
    
    except Exception as e:
        db.session.rollback()
        print(f"Error updating student: {e}")
        return False


def delete_student(id):
    student = get_student(id)
    if not student:
        return None

    db.session.delete(student)
    db.session.commit()
    return True
