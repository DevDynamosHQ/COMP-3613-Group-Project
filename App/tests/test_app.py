import unittest
from App.models import User, Student, Staff, Employer, Position, Application
from App.models.application_state import AppliedState, ShortlistedState, AcceptedState, RejectedState
from App.models.position import PositionStatus
from werkzeug.security import generate_password_hash


class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass", "user")
        assert user.username == "bob"
        assert user.role == "user"

    def test_new_student(self):
        student = Student("john", "johnpass")
        assert student.username == "john"
        assert student.role == "student"

    def test_new_staff(self):
        staff = Staff("jim", "jimpass")
        assert staff.username == "jim"
        assert staff.role == "staff"

    def test_new_employer(self):
        employer = Employer("alice", "alicepass")
        assert employer.username == "alice"
        assert employer.role == "employer"

    def test_user_get_json(self):
        user = User("bob", "bobpass", "user")
        user_json = user.get_json()
        assert user_json["username"] == "bob"
        assert user_json["role"] == "user"
        assert "id" in user_json

    def test_hashed_password(self):
        password = "mypass"
        user = User("bob", password, "user")
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password, "user")
        assert user.check_password(password)

    def test_check_wrong_password(self):
        user = User("bob", "mypass", "user")
        assert not user.check_password("wrongpass")

    def test_set_password(self):
        user = User("bob", "oldpass", "user")
        old_hash = user.password
        user.set_password("newpass")
        assert user.password != old_hash
        assert user.check_password("newpass")


class StudentUnitTests(unittest.TestCase):

    def test_new_student_default_role(self):
        student = Student("john", "johnpass")
        assert student.role == "student"

    def test_student_get_json(self):
        student = Student("john", "johnpass")
        student.email = "john@example.com"
        student.degree = "Computer Science"
        student_json = student.get_json()
        assert student_json["username"] == "john"
        assert student_json["role"] == "student"
        assert student_json["email"] == "john@example.com"
        assert student_json["degree"] == "Computer Science"

    def test_student_calculate_age_none(self):
        student = Student("john", "johnpass")
        assert student.calculate_age() is None

    def test_student_calculate_age(self):
        from datetime import date
        student = Student("john", "johnpass")
        student.dob = date(2000, 1, 1)
        age = student.calculate_age()
        assert age >= 24  

    def test_student_cannot_shortlist(self):
        student = Student("john", "johnpass")
        application = Application(1, 1)
        assert not student.can_shortlist_application(application)

    def test_student_cannot_accept(self):
        student = Student("john", "johnpass")
        application = Application(1, 1)
        assert not student.can_accept_application(application)

    def test_student_cannot_reject(self):
        student = Student("john", "johnpass")
        application = Application(1, 1)
        assert not student.can_reject_application(application)


class StaffUnitTests(unittest.TestCase):

    def test_new_staff_default_role(self):
        staff = Staff("jim", "jimpass")
        assert staff.role == "staff"

    def test_staff_get_json(self):
        staff = Staff("jim", "jimpass")
        staff.email = "jim@example.com"
        staff_json = staff.get_json()
        assert staff_json["username"] == "jim"
        assert staff_json["role"] == "staff"
        assert staff_json["email"] == "jim@example.com"

    def test_staff_can_shortlist(self):
        staff = Staff("jim", "jimpass")
        application = Application(1, 1)
        assert staff.can_shortlist_application(application)

    def test_staff_cannot_accept(self):
        staff = Staff("jim", "jimpass")
        application = Application(1, 1)
        assert not staff.can_accept_application(application)

    def test_staff_cannot_reject(self):
        staff = Staff("jim", "jimpass")
        application = Application(1, 1)
        assert not staff.can_reject_application(application)


class EmployerUnitTests(unittest.TestCase):

    def test_new_employer_default_role(self):
        employer = Employer("alice", "alicepass")
        assert employer.role == "employer"

    def test_employer_get_json(self):
        employer = Employer("alice", "alicepass")
        employer.company_name = "Tech Corp"
        employer.email = "alice@techcorp.com"
        employer.phone = "555-1234"
        employer_json = employer.get_json()
        assert employer_json["username"] == "alice"
        assert employer_json["role"] == "employer"
        assert employer_json["company_name"] == "Tech Corp"
        assert employer_json["email"] == "alice@techcorp.com"
        assert employer_json["phone"] == "555-1234"

    def test_employer_cannot_shortlist(self):
        employer = Employer("alice", "alicepass")
        application = Application(1, 1)
        assert not employer.can_shortlist_application(application)

    def test_employer_can_accept(self):
        employer = Employer("alice", "alicepass")
        application = Application(1, 1)
        assert employer.can_accept_application(application)

    def test_employer_can_reject(self):
        employer = Employer("alice", "alicepass")
        application = Application(1, 1)
        assert employer.can_reject_application(application)


class PositionUnitTests(unittest.TestCase):

    def test_new_position(self):
        position = Position("Software Developer", "Build apps", 10, 5)
        assert position.title == "Software Developer"
        assert position.description == "Build apps"
        assert position.employer_id == 10
        assert position.number_of_positions == 5
        assert position.status == PositionStatus.open

    def test_new_position_default_status(self):
        position = Position("Developer", "Code", 1, 3)
        assert position.status == PositionStatus.open

    def test_position_get_json(self):
        position = Position("Software Developer", "Build apps", 10, 5)
        position.id = 1
        position_json = position.get_json()
        assert position_json["title"] == "Software Developer"
        assert position_json["description"] == "Build apps"
        assert position_json["employer_id"] == 10
        assert position_json["number_of_positions"] == 5
        assert position_json["status"] == "open"
        assert position_json["id"] == 1

    def test_position_closed_status(self):
        position = Position("Developer", "Code", 1, 3, PositionStatus.closed)
        assert position.status == PositionStatus.closed
        assert position.get_json()["status"] == "closed"


class ApplicationStateUnitTests(unittest.TestCase):

    def test_applied_state_name(self):
        state = AppliedState()
        assert state.get_state_name() == "applied"

    def test_applied_state_can_shortlist(self):
        state = AppliedState()
        assert state.can_shortlist() == True
        assert state.can_accept() == False
        assert state.can_reject() == False

    def test_applied_to_shortlisted(self):
        application = Application(1, 1)
        state = AppliedState()
        state.shortlist(application)
        assert isinstance(application._state, ShortlistedState)

    def test_applied_cannot_accept(self):
        application = Application(1, 1)
        state = AppliedState()
        with self.assertRaises(ValueError):
            state.accept(application)

    def test_applied_cannot_reject(self):
        application = Application(1, 1)
        state = AppliedState()
        with self.assertRaises(ValueError):
            state.reject(application)

    def test_shortlisted_state_name(self):
        state = ShortlistedState()
        assert state.get_state_name() == "shortlisted"

    def test_shortlisted_state_permissions(self):
        state = ShortlistedState()
        assert state.can_shortlist() == False
        assert state.can_accept() == True
        assert state.can_reject() == True

    def test_shortlisted_to_accepted(self):
        application = Application(1, 1)
        application._state = ShortlistedState()
        application._state.accept(application)
        assert isinstance(application._state, AcceptedState)

    def test_shortlisted_to_rejected(self):
        application = Application(1, 1)
        application._state = ShortlistedState()
        application._state.reject(application)
        assert isinstance(application._state, RejectedState)

    def test_shortlisted_cannot_shortlist_again(self):
        application = Application(1, 1)
        state = ShortlistedState()
        with self.assertRaises(ValueError):
            state.shortlist(application)

    def test_accepted_state_name(self):
        state = AcceptedState()
        assert state.get_state_name() == "accepted"

    def test_accepted_state_permissions(self):
        state = AcceptedState()
        assert state.can_shortlist() == False
        assert state.can_accept() == False
        assert state.can_reject() == False

    def test_accepted_cannot_shortlist(self):
        application = Application(1, 1)
        state = AcceptedState()
        with self.assertRaises(ValueError):
            state.shortlist(application)

    def test_accepted_cannot_accept_again(self):
        application = Application(1, 1)
        state = AcceptedState()
        with self.assertRaises(ValueError):
            state.accept(application)

    def test_accepted_cannot_reject(self):
        application = Application(1, 1)
        state = AcceptedState()
        with self.assertRaises(ValueError):
            state.reject(application)

    def test_rejected_state_name(self):
        state = RejectedState()
        assert state.get_state_name() == "rejected"

    def test_rejected_state_permissions(self):
        state = RejectedState()
        assert state.can_shortlist() == False
        assert state.can_accept() == False
        assert state.can_reject() == False

    def test_rejected_cannot_shortlist(self):
        application = Application(1, 1)
        state = RejectedState()
        with self.assertRaises(ValueError):
            state.shortlist(application)

    def test_rejected_cannot_accept(self):
        application = Application(1, 1)
        state = RejectedState()
        with self.assertRaises(ValueError):
            state.accept(application)

    def test_rejected_cannot_reject_again(self):
        application = Application(1, 1)
        state = RejectedState()
        with self.assertRaises(ValueError):
            state.reject(application)


class ApplicationUnitTests(unittest.TestCase):

    def test_new_application(self):
        application = Application(1, 2)
        assert application.student_id == 1
        assert application.position_id == 2
        assert application.state_name == "applied"
        assert isinstance(application._state, AppliedState)

    def test_application_initial_state(self):
        application = Application(5, 10)
        assert application.state_name == "applied"
        assert application.state.can_shortlist() == True

    def test_application_get_state_from_name(self):
        application = Application(1, 1)
        state = application._get_state_from_name("shortlisted")
        assert isinstance(state, ShortlistedState)

    def test_application_state_property(self):
        application = Application(1, 1)
        application.state_name = "shortlisted"
        state = application.state
        assert isinstance(state, ShortlistedState)

    def test_application_can_user_shortlist_staff(self):
        application = Application(1, 1)
        staff = Staff("jim", "jimpass")
        staff.id = 1
        assert application.can_user_shortlist(staff) == True

    def test_application_can_user_shortlist_non_staff(self):
        application = Application(1, 1)
        student = Student("john", "johnpass")
        assert application.can_user_shortlist(student) == False

    def test_application_can_user_accept_employer(self):
        application = Application(1, 1)
        application.state_name = "shortlisted"
        employer = Employer("alice", "alicepass")
        employer.id = 1
        assert application.can_user_accept(employer) == True

    def test_application_can_user_accept_non_employer(self):
        application = Application(1, 1)
        application.state_name = "shortlisted"
        staff = Staff("jim", "jimpass")
        assert application.can_user_accept(staff) == False

    def test_application_shortlist_with_staff(self):
        application = Application(1, 1)
        staff = Staff("jim", "jimpass")
        staff.id = 5
        result = application.shortlist(user=staff)
        assert result == "shortlisted"
        assert application.staff_id == 5

    def test_application_shortlist_permission_error(self):
        application = Application(1, 1)
        student = Student("john", "johnpass")
        student.username = "john"
        with self.assertRaises(PermissionError):
            application.shortlist(user=student)

    def test_application_accept_with_employer(self):
        application = Application(1, 1)
        application.state_name = "shortlisted"
        employer = Employer("alice", "alicepass")
        employer.id = 1
        result = application.accept(user=employer)
        assert result == "accepted"

    def test_application_reject_with_employer(self):
        application = Application(1, 1)
        application.state_name = "shortlisted"
        employer = Employer("alice", "alicepass")
        employer.id = 1
        result = application.reject(user=employer)
        assert result == "rejected"

    def test_application_get_json(self):
        application = Application(1, 2)
        application.id = 10
        application.staff_id = 3
        app_json = application.get_json()
        assert app_json["id"] == 10
        assert app_json["student_id"] == 1
        assert app_json["position_id"] == 2
        assert app_json["staff_id"] == 3
        assert app_json["state"] == "applied"
        assert app_json["can_shortlist"] == True
        assert app_json["can_accept"] == False
        assert app_json["can_reject"] == False

    def test_application_full_workflow(self):
        application = Application(1, 1)
        staff = Staff("jim", "jimpass")
        staff.id = 5
        employer = Employer("alice", "alicepass")
        employer.id = 10
        
        
        application.shortlist(user=staff)
        assert application.state_name == "shortlisted"
        assert application.staff_id == 5
        
        
        application.accept(user=employer)
        assert application.state_name == "accepted"


if __name__ == "__main__":
    unittest.main()
