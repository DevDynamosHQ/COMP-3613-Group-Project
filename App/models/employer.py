from App.database import db
from App.models.user import User

class Employer(User):

    __tablename__ = 'employer'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
   
    company_name = db.Column(db.String(256))
    email = db.Column(db.String(256))
    phone = db.Column(db.String(256))

    positions = db.relationship("Position", back_populates="employer")
   

    __mapper_args__ = {
        "polymorphic_identity": "employer",
    }


    def __init__(self, username, password, role="employer"):
        super().__init__(username, password, role)


    def can_shortlist_application(self, application):
        return False
    
    
    def can_accept_application(self, application):
        return True
    

    def can_reject_application(self, application):
        return True


    def get_json(self):
        base_json = super().get_json()
        employer_json = {
            "company_name": self.company_name,
            "email": self.email,
            "phone": self.phone,
            "positions": [p.get_json() for p in self.positions]
        }
        return {**base_json, **employer_json}


    def __repr__(self):
        return f"<Employer {self.id}: {self.username}>"

