from App.models import Employer
from App.database import db


def create_employer(username, user_id):
    employer = Employer(
        username=username,
        user_id=user_id
    )
    db.session.add(employer)
    db.session.commit()
    return employer


def get_employer(id):
    return db.session.get(Employer, id)


def get_employer_by_user(user_id):
    return db.session.execute(
        db.select(Employer).filter_by(user_id=user_id)
    ).scalar_one_or_none()


def get_all_employers():
    return db.session.scalars(
        db.select(Employer)
    ).all()


def get_all_employers_json():
    employers = get_all_employers()
    return [e.get_json() for e in employers]


def update_employer(id, username=None):
    employer = get_employer(id)
    if not employer:
        return None

    if username is not None:
        employer.username = username

    db.session.commit()
    return employer


def delete_employer(id):
    employer = get_employer(id)
    if not employer:
        return None

    db.session.delete(employer)
    db.session.commit()
    return True
