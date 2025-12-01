from App.database import db

from .application_state import AppliedState, ShortlistedState, AcceptedState, RejectedState

class Application(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)
    state_name = db.Column(db.String(50), nullable=False, default="applied")
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    student = db.relationship('Student', backref=db.backref('applications', lazy=True))
    position = db.relationship('Position', backref=db.backref('applications', lazy=True))
    staff = db.relationship('Staff', backref=db.backref('applications', lazy=True))

    def __init__(self, student_id, position_id, **kwargs):
        super(Application, self).__init__(**kwargs)
        self.student_id = student_id
        self.position_id = position_id
        self.state_name = 'applied'
        self._state = AppliedState()

    def _get_state_from_name(self, state_name):
        state_map = {
            'applied' : AppliedState(),
            'shortlisted' : ShortlistedState(),
            'accepted' : AcceptedState(),
            'rejected' : RejectedState()
        }
        return state_map.get(state_name, AppliedState())
    
    @property
    def state(self):
        if not hasattr(self, '_state') or self._state.get_state_name() != self.state_name:
            self._state = self._get_state_from_name(self.state_name)
        return self._state
    
    def can_user_shortlist(self, user):
        return user.role == 'staff' and self.state.can_shortlist()
    
    def can_user_accept(self, user):
        return user.role == 'employer' and self.state.can_accept()
    
    def can_user_reject(self, user):
        return user.role == 'employer' and self.state.can_reject()
    

    def shortlist(self, user=None):
        if user and not self.can_user_shortlist(user):
            raise PermissionError(f"User '{user.username}' cannot shortlist this application.")
        self.staff_id = user.id if user else self.staff_id
        self.state.shortlist(self)
        self.state_name = self._state.get_state_name()
       # db.session.commit()
        return self.state_name
    
    def accept(self, user=None):
        if user and not self.can_user_accept(user):
            raise PermissionError(f"User '{user.username}' cannot accept this application.")
        self.state.accept(self)
        self.state_name = self._state.get_state_name()
       # db.session.commit()
        return self.state_name
    
    def reject(self, user=None):
        if user and not self.can_user_reject(user):
            raise PermissionError(f"User '{user.username}' cannot reject this application.")
        self.state.reject(self)
        self.state_name = self._state.get_state_name()
        #db.session.commit()
        return self.state_name
    
    def get_json(self):
        return {
            'id' : self.id,
            'student_id' : self.student_id,
            'position_id' : self.position_id,
            'staff_id' : self.staff_id,
            'state' : self.state_name,
            'created_at' : self.created_at.isoformat() if self.created_at else None,
            'updated_at' : self.updated_at.isoformat() if self.updated_at else None,
            'can_shortlist' : self.state.can_shortlist(),
            'can_accept' : self.state.can_accept(),
            'can_reject' : self.state.can_reject(),
        }
    
    def __repr__(self):
        return f'<Application {self.id}: Student {self.student_id} ({self.state_name})>'
    
