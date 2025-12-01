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
    description = db.Column(db.Text, nullable=True)
    number_of_positions = db.Column(db.Integer, nullable=False)
    status = db.Column(Enum(PositionStatus, native_enum=False), nullable=False, default=PositionStatus.open)
   
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)

    employer = db.relationship("Employer", back_populates="positions")


    def __init__(self, title, description, employer_id, number_of_positions, status=PositionStatus.open):
        self.title = title
        self.description = description
        self.employer_id = employer_id
        self.number_of_positions = number_of_positions
        self.status = status
        
        

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


    def get_json(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'description' : self.description,
            'number_of_positions' : self.number_of_positions,
            'status' : self.status.value,
            'employer_id' : self.employer_id
        }

    def __repr__(self):
        return f"<Position {self.id}: {self.title} ({self.status.value}) posted by Employer {self.employer_id}>"