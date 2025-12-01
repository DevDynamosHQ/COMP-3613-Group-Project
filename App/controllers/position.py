from App.models import Position, Employer
from App.database import db
from App.models.position import PositionStatus

def open_position(employer_id, title, number_of_positions, description=None):
    new_position = Position(title=title, number_of_positions=number_of_positions, employer_id=employer_id, description=description)
    db.session.add(new_position)

    try:
        db.session.commit()
        return new_position
    
    except Exception as e:
        db.session.rollback()
        print(f"Error creating position: {e}")
        return None

def get_position(position_id):
    return db.session.get(Position, position_id)


def get_positions_by_employer(employer_id):
    return db.session.query(Position).filter_by(employer_id=employer_id).all()

def get_all_positions():
    return db.session.query(Position).all()


def get_all_open_positions():
    return db.session.query(Position).filter_by(status=PositionStatus.open).all()


def get_positions_by_employer_json(employer_id):
    positions = get_positions_by_employer(employer_id)
    return [position.get_json() for position in positions] if positions else []


def get_all_positions_json():
    positions = get_all_positions()
    return [position.get_json() for position in positions] if positions else []


def update_position(position_id, employer_id, title=None, description=None, number_of_positions=None, status=None):
    position = get_position(position_id)

    if not position:
        return False
    
    if employer_id is None or position.employer_id != employer_id:
        return False
    
    if title is not None:
        position.title = title

    if description is not None:
        position.description = description

    if number_of_positions is not None:
        position.number_of_positions = number_of_positions

    if status is not None:
        position.status = PositionStatus(status)

    try:
        db.session.commit()
        return True
    
    except Exception as e:
        db.session.rollback()
        print(f"Error updating position: {e}")
        return False
    