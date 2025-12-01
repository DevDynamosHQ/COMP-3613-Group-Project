from App.database import db
from sqlalchemy import Enum
import enum

class PositionStatus(enum.Enum):
    open = "open"
    closed = "closed"

class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    number_of_positions = db.Column(db.Integer, default=1)
    status = db.Column(Enum(PositionStatus, native_enum=False), nullable=False, default=PositionStatus.open)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    number = db.Column(db.Integer) 
    position_id = db.Column(db.Integer) 
    #employer = db.relationship("Employer", back_populates="positions")
    employer = db.relationship('User', foreign_keys=[employer_id], back_populates='positions')
    #employer = db.relationship('User', foreign_keys=[employer_id], backref=db.backref('employer_positions', lazy=True))

    def __init__(self, title, employer_id, number, position_id):
        self.title = title
        self.employer_id = employer_id
        self.status = PositionStatus.open
        self.number_of_positions = number
        self.number = number
        self.position_id = position_id
        
    
    
        

    def update_status(self, status):
        if isinstance(status, PositionStatus):
            self.status = status
        else:
            stat = PositionStatus(status)
            if isinstance(stat, PositionStatus):
                self.status = stat
        db.session.commit()
        return self.status.value

    def update_number_of_positions(self, number_of_positions):
        self.number_of_positions = number_of_positions
        db.session.commit()
        return self.number_of_positions

    def delete_position(self):
        db.session.delete(self)
        db.session.commit()
        return

    def list_positions(self):
        return db.session.query(self).all()

    def toJSON(self):
        return {
            "id": self.id,
            "title": self.title,
            "number_of_positions": self.number_of_positions,
            "status": self.status.value,
            "employer_id": self.employer_id,
            "number": self.number,
            "position_id": self.position_id
        }

    def __repr__(self):
        return f"<Position {self.id}: {self.title} ({self.status.value}) posted by Employer {self.employer_id}>"