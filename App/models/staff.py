from App.database import db
from App.models.user import User

class Staff(User):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    email = db.Column(db.String(256))
    profile_pic = db.Column(db.String(255))



    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }


    def __init__(self, username, password, role="staff"):
        super().__init__(username, password, role)

    
    def can_shortlist_application(self, application):
        return True
    

    def can_accept_application(self, application):
        return False
    

    def can_reject_application(self, application):
        return False


    def get_json(self):
        base_json = super().get_json()
        staff_json = {
            "email": self.email,
            "profile_pic" : self.profile_pic
        }
        return {**base_json, **staff_json}


    def __repr__(self):
        return f"<Staff {self.id}: {self.username}>"
