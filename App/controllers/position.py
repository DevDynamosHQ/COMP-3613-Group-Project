from App.models import Position, Employer, PositionStatus
from App.database import db

def create_new_position(user_id, title, number_of_positions, position_id):
    employer = Employer.query.filter_by(user_id=user_id).first()
    if not employer:
        return None
    new_position = Position(title, employer.id, number_of_positions, position_id)
    db.session.add(new_position)
    try:
        db.session.commit()
        return new_position
    except Exception as e:
        db.session.rollback()
        return None

def open_position(user_id, position_id):
    stat = PositionStatus.open
    employer = Employer.query.filter_by(user_id=user_id).first()
    if not employer:
        return None
    
    position = Position.query.filter_by(position_id = position_id).first()
    if not position:
        return None
    
    if position.status == stat:
        return position
    
    try:
        position.update_status(stat)
        return position
    except Exception:
        db.session.rollback()
        return None
    


def get_positions_by_employer(user_id):
    employer = Employer.query.filter_by(user_id=user_id).first()
    return db.session.query(Position).filter_by(employer_id=employer.id).all()

def get_all_positions():
    return Position.query.all()

def get_all_positions_json():
    positions = Position.query.all()
    if positions:
        return [position.toJSON() for position in positions]
    return []

def get_positions_by_employer_json(user_id):
    employer = Employer.query.filter_by(user_id=user_id).first()
    positions = db.session.query(Position).filter_by(employer_id=employer.id).all()
    if positions:
        return [position.toJSON() for position in positions]
    return []

def close_position(user_id, position_id):
    stat = PositionStatus.close
    employer = Employer.query.filter_by(user_id=user_id).first()
    if not employer:
        return None
    
    position = Position.query.filter_by(position_id = position_id).first()
    if not position:
        return None
    
    if position.status == stat:
        return position
    
    try:
        position.update_status(stat)
        return position
    except Exception:
        db.session.rollback()
        return None