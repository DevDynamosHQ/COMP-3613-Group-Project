from sqlalchemy import false
from App.models import Shortlist, Position, Staff, Student
from App.database import db


def add_student_to_shortlist(student_id, position_id, staff_id):

    teacher = db.session.get(Staff, staff_id)
    student = db.session.get(Student, student_id)

    if not student or not teacher:
        return False

    existing = db.session.execute(
        db.select(Shortlist).filter_by(student_id=student.id, position_id=position_id)
    ).scalar_one_or_none()

    position = db.session.execute(
        db.select(Position)
        .filter(
            Position.id == position_id,
            Position.number_of_positions > 0,
            Position.status == "open"
        )
    ).scalar_one_or_none()

    if existing or not position:
        return False

    shortlist = Shortlist(
        student_id=student.id,
        position_id=position.id,
        staff_id=teacher.id,
        title=position.title
    )

    db.session.add(shortlist)
    db.session.commit()
    return shortlist


def decide_shortlist(student_id, position_id, decision):

    shortlist = db.session.execute(
        db.select(Shortlist)
        .filter_by(student_id=student_id, position_id=position_id, status="pending")
    ).scalar_one_or_none()

    position = db.session.get(Position, position_id)

    if not shortlist or not position or position.number_of_positions <= 0:
        return False

    shortlist.update_status(decision)
    position.update_number_of_positions(position.number_of_positions - 1)

    db.session.commit()
    return shortlist

def get_shortlist_by_student(student_id):
    return db.session.execute(
            db.select(Shortlist).filter_by(student_id=student_id)
        ).scalars().all()


def get_shortlist_by_position(position_id):
    return db.session.execute(
        db.select(Shortlist).filter_by(position_id=position_id)
    ).scalars().all()
