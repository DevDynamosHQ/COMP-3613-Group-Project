from email.mime import base
from App.database import db
from App.models.user import User

class Staff(User):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    
    email = db.Column(db.String(256))


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
            "email": self.email
        }
        return {**base_json, **staff_json}


    def __repr__(self):
        return f"<Staff {self.id}: {self.username}>"

'''
from App.database import db
from App.models.user import User
from App.models.application import Application
from App.models.position import Position
from App.models.student import Student

class Staff(User):
    #__tablename__ = 'staff'
    #id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    #username = db.Column(db.String(20), nullable=False, unique=True)
    #role = db.Column(db.String(50), nullable=False, default="staff")
    #password = db.Column(db.String(128), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }

    def __init__(self, username, user_id, password):
        self.username = username
        self.user_id = user_id
        self.password = password
        self.role = "staff"

    def __init__(self, username, password):
        # Call parent constructor - remove user_id parameter
        super().__init__(username, password, "staff")

    def add_to_shortlist(self, student_id, position_id):
        student = db.session.get(Student, student_id)
        position = db.session.get(Position, position_id)
        if not student or not position:
            return False

        existing = db.session.execute(db.select(Application).filter_by(student_id=student.id, position_id=position.id))
        if existing:
            return False

        application = Application(student_id=student.id, position_id=position.id, staff_id=self.id, title=position.title)
        db.session.add(application)
        db.session.commit()
        return application
    
    def can_shortlist_application(self, application):
        return True
    
    def can_accept_application(self, application):
        return False
    
    def can_reject_application(self, application):
        return False

    def get_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username
        }

    def get_json(self):
        return super().get_json()

    def __repr__(self):
        return f"<Staff {self.id}: {self.username}>"
'''