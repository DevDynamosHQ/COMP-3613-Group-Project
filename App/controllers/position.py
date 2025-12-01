from App.models import User, Position, Employer, PositionStatus
from App.database import db
'''
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
'''
def create_new_position(employer_id, title, number, position_id):

    employer = User.query.get(employer_id)
    
    if not employer or employer.role != "employer":
        return None
    
    new_position = Position(
        title=title,
        employer_id=employer_id,  
        number=number,
        position_id=position_id
    )
    
    db.session.add(new_position)
    try:
        db.session.commit()
        return new_position
    except Exception as e:
        db.session.rollback()
        print(f"Error creating position: {e}")
        return None
def open_position(employer_id, position_id):
    #stat = PositionStatus.open
    employer = User.query.get(employer_id)
    if not employer or employer.role != "employer":
        return None
    
    position = Position.query.get(position_id)
    if not position:
        return None
    
    if position.employer_id != employer.id:
        return None 

    try:
        
        position.status = "open" 
        db.session.commit()
        return position
    except Exception as e:
        db.session.rollback()
        print(f"Error opening position: {e}")
        return None

    


def get_positions_by_employer(employer_id):
    #employer = Employer.query.filter_by(user_id=user_id).first()
    return Position.query.filter_by(employer_id=employer.id).all()

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
    #stat = PositionStatus.closed
    employer = Employer.query.get(employer_id)
    if not employer or employer.role != "employer":
        return None
    
    position = Position.query.get(position_id)
    if not position:
        return None
    
    if position.employer_id != employer.id:
        return None
    
    try:
        position.status = "closed"
        db.session.commit()
        return position
    except Exception as e:
        db.session.rollback()
        print(f"Error closing position: {e}")
        return None