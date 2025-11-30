from App.models import Student
from App.database import db

#edited

def create_student(username, password, id):
    student = Student(username=username, user_id=id, password=password)
    db.session.add(student)
    db.session.commit()
    return student


def get_student(id):
    return db.session.get(Student, id)

def get_student_by_user(user_id):
    return db.session.execute(
        db.select(Student).filter_by(user_id=user_id)
    ).scalar_one_or_none()

def get_all_students():
    return db.session.scalars(db.select(Student)).all()

def get_all_students_json():
    students = get_all_students()
    return [s.get_json() for s in students]


def update_student(id, email=None, dob=None, gender=None, degree=None, phone=None, gpa=None, resume=None):
    student = get_student(id)

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

    db.session.commit()
    return student


def delete_student(id):
    student = get_student(id)
    if not student:
        return None

    db.session.delete(student)
    db.session.commit()
    return True
