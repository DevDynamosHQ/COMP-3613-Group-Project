from App.database import db
from App.models.user import User

class Employer(db.Model):
    __tablename__ = 'employer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    positions = db.relationship("Position", back_populates="employer")

    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id

    def create_position(self, title, number_of_positions=1):
        new_position = Position(
            title=title,
            employer_id=self.id,
            number_of_positions=number_of_positions
        )
        db.session.add(new_position)
        db.session.commit()
        return new_position
    
    def close_position(self, position_id):
        position = Position.query.filter_by(id=position_id, employer_id=self.id).first()
        if not position:
            raise ValueError("Position not found or does not belong to this employer.")
        position.close()  # delegate to Position's state pattern
        db.session.commit()
        return position
    
    def toJSON(self):
        return {
            "id": self.id,
            "username": self.username,
            "user_id": self.user_id,
            "positions": [position.toJSON() for position in self.positions]
        }

    def __repr__(self):
        return f"<Employer {self.id}: {self.username}>"