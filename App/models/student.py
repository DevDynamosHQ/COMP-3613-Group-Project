from App.database import db
from App.models.user import User
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date

class Student(User):
    __tablename__ = 'student'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    
    email = db.Column(db.String(256))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(256))
    degree = db.Column(db.String(256))
    phone = db.Column(db.String(256))
    gpa = db.Column(db.Float)
    resume = db.Column(db.String(256))


    __mapper_args__ = {
        "polymorphic_identity": "student",
    }


    def __init__(self, username, password, role="student"):
        super().__init__(username, password, role)


    def can_shortlist_application(self, application):
        return False
    

    def can_accept_application(self, application):
        return False
    

    def can_reject_application(self, application):
        return False
    

    def calculate_age(self):
        if not self.dob:
            return None
        today = date.today()
        return today.year - self.dob.year - (
            (today.month, today.day) < (self.dob.month, self.dob.day)
        )
    

    def get_json(self):
        base_json = super().get_json()
        student_json = {
            'email': self.email,
            'degree': self.degree,
            'phone': self.phone,
            'gender': self.gender,
            'gpa': self.gpa,
            'resume': self.resume,
            'age': self.calculate_age()
        }
        return {**base_json, **student_json}
    

    def __repr__(self):
        return f"<Student {self.id}: {self.username}>"
    


    
'''
from App.database import db
from App.models.user import User
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date

#edited.
class Student(User):
    #__tablename__ = 'student'
    #id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    #username =  db.Column(db.String(20), nullable=False, unique=True)
    #email = db.Column(db.String(256))
    #dob = db.Column(db.Date)
    #gender = db.Column(db.String(256))
    #degree = db.Column(db.String(256))
    #phone = db.Column(db.String(256))
    #gpa = db.Column(db.Float)
    #resume = db.Column(db.String(256))
    #password = db.Column(db.String(256), nullable=False)
    #role = db.Column(db.String(50), nullable=False, default="student")


    __mapper_args__ = {
        "polymorphic_identity": "student",
    }

    def __init__(self, username, user_id, password):
        self.username = username
        self.user_id = user_id
        self.password = password
        self.role = "student"

    def __init__(self, username, password):
        # Call parent constructor - remove user_id parameter
        super().__init__(username, password, "student")

    def can_shortlist_application(self, application):
        return False
    
    def can_accept_application(self, application):
        return False

    def can_reject_application(self, application):
        return False



    def age(self):
        if not self.dob:
            return None
        today = date.today()
        return today.year - self.dob.year - (
            (today.month, today.day) < (self.dob.month, self.dob.day)
        )


    def get_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            #'email': self.email,
            #'degree': self.degree,
            #'phone': self.phone,
            #'gender': self.gender,
            #'gpa': self.gpa,
            #'resume': self.resume,
            #'age': self.age
        }

    def get_json(self):
        base_json = super().get_json()
        # Add student-specific fields
        student_json = {
            'email': self.email,
            'degree': self.degree,
            'phone': self.phone,
            'gender': self.gender,
            'gpa': self.gpa,
            'resume': self.resume,
            'age': self.age()
        }
        return {**base_json, **student_json}
#    def update_DOB(self, date):
#        self.DOB = date
#        db.session.commit()
#        return self.DOB
#        
#   @hybrid_property
#   def age(self):
#       if self.DOB is None:
#           return None
#       today = date.today()
#       dob = self.DOB
#       return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

'''