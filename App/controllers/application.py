import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.models import Staff, Student, Position
#from App.main import create_app
#from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, open_position, add_student_to_shortlist, decide_shortlist, get_shortlist_by_student, get_shortlist_by_position, get_positions_by_employer)
from App.models.application import Application

from App.models.application_state import AppliedState, ShortlistedState, AcceptedState, RejectedState

from App.controllers.user import (
    create_user, 
    get_all_users_json, 
    get_all_users
)

from App.controllers.initialize import initialize

from App.controllers.position import (
    open_position,
    get_positions_by_employer
)
# This commands file allow you to create convenient CLI commands for testing controllers

#app = create_app()
#migrate = get_migrate(app)


def add_student_to_shortlist(student_id, position_id, staff_id):

    teacher = db.session.get(Staff, staff_id)
    student = db.session.get(Student, student_id)

    if not student or not teacher:
        return False

    existing = db.session.execute(
        db.select(Application).filter_by(student_id=student.id, position_id=position_id)
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

    shortlist = Application(
        student_id=student.id,
        position_id=position.id,
        staff_id=teacher.id,
        title=position.title, 
        state_name = "shortlisted",
        _state = ShortlistedState()
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

