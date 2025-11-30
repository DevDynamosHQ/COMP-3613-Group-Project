from App.database import db
from App.models.user import User

class Employer(db.Model):
    __tablename__ = 'employer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    positions = db.relationship("Position", back_populates="employer")
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="employer")

    def __init__(self, username, password, user_id):
        self.username = username
        self.password = password
        self.user_id = user_id
        self.role = "employer"

    def can_shortlist_application(self, application):
        return False
    
    def can_accept_application(self, application):
        return True
    
    def can_reject_application(self, application):
        return True

    def toJSON(self):
        return {
            "id": self.id,
            "username": self.username,
            "user_id": self.user_id,
            "positions": [position.toJSON() for position in self.positions]
        }

    def __repr__(self):
        return f"<Employer {self.id}: {self.username}>"