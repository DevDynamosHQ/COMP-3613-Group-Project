from datetime import date
import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash


from App.main import create_app
from App.database import db, create_db

from App.models import User, Student, Staff, Employer, Position, Application, PositionStatus

from App.controllers.user import create_user
from App.controllers.position import open_position, get_position
from App.controllers.application import create_application, get_application, shortlist_application, accept_application


LOGGER = logging.getLogger(__name__)


'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    
    with app.app_context():
        create_db()
        yield app.test_client()
        db.drop_all()


class ApplicationControllerIntegrationTests(unittest.TestCase):
     
    def create_test_student(self, username="hannah", password="hannahpass"):
        student = create_user(username, password, "student")
        assert student is not None
        return student
     

    def create_test_employer(self, username="sam", password="sampass"):
        employer = create_user(username, password, "employer")
        assert employer is not None
        return employer
     
    def create_test_staff(self, username="rick", password="rickpass"):
        staff = create_user(username, password, "staff")
        assert staff is not None
        return staff


    def create_test_position(self, employer, title="Developer", number_of_positions=1):
        position = open_position(employer.id, title, number_of_positions)
        assert position is not None
        return position


    # Test creating a valid application
    def test_create_application_valid(self):
        student = self.create_test_student()
        employer = self.create_test_employer()

        position = self.create_test_position(employer, title="Developer", number_of_positions=2)

        application = create_application(student.id, position.id)
        assert application is not None

        stored_application = get_application(application.id)
        assert stored_application is not None

        assert stored_application.student_id == student.id
        assert stored_application.position_id == position.id

        assert application.student_id == student.id
        assert application.position_id == position.id

    
    # Test creating applications with invalid inputs
    def test_create_application_invalid(self):
        student = self.create_test_student()
        employer = self.create_test_employer()
        position = self.create_test_position(employer, number_of_positions=2)

        # Non-existent student
        invalid_app = create_application(9999, position.id)
        assert invalid_app is None

        # Non-existent position
        invalid_app = create_application(student.id, 9999)
        assert invalid_app is None

        # Position with no slots
        position.number_of_positions = 0
        db.session.commit()

        invalid_app = create_application(student.id, position.id)
        assert invalid_app is None

    
    # Test shortlisting a valid application
    def test_shortlist_application_valid(self):
        student = self.create_test_student()
        staff = self.create_test_staff()
        employer = self.create_test_employer()
        position = self.create_test_position(employer, number_of_positions=2)

        application = create_application(student.id, position.id)
        assert application is not None

        shortlisted = shortlist_application(application.id, staff.id)
        assert shortlisted is not None

        stored_application = get_application(shortlisted.id)
        assert stored_application.id == application.id

    
    # Test shortlisting with invalid inputs
    def test_shortlist_application_invalid(self):
        student = self.create_test_student()
        staff = self.create_test_staff()
        employer = self.create_test_employer()
        position = self.create_test_position(employer, number_of_positions=2)

        application = create_application(student.id, position.id)
        assert application is not None

        # Non-existent staff
        invalid_shortlist = shortlist_application(application.id, 9999)
        assert invalid_shortlist is None

        # Non-existent application
        invalid_shortlist = shortlist_application(9999, staff.id)
        assert invalid_shortlist is None

        # Both staff and application do not exist
        invalid_shortlist = shortlist_application(9999, 9999)
        assert invalid_shortlist is None

        # Application already shortlisted 
        shortlisted_once = shortlist_application(application.id, staff.id)
        assert shortlisted_once is not None

        # Duplicates prevented
        duplicate_shortlist = shortlist_application(application.id, staff.id)
        assert duplicate_shortlist is None  

    
    # Test accepting a valid application
    def test_accept_application_valid(self):
        student = self.create_test_student()
        staff = self.create_test_staff()
        employer = self.create_test_employer()
        position = self.create_test_position(employer, number_of_positions=2)

        application = create_application(student.id, position.id)
        assert application is not None

        shortlisted = shortlist_application (application.id, staff.id)
        assert shortlisted is not None

        accepted = accept_application(application.id, employer.id)
        assert accepted is not None
        assert accepted.state_name == "accepted"

        stored_position = get_position(position.id)
        assert stored_position.number_of_positions == 1

        stored_application = get_application(application.id)
        assert stored_application.state_name == "accepted"

    
    # Test accepting application with invalid inputs
    def test_accept_application_invalid(self):
        student = self.create_test_student()
        employer = self.create_test_employer()
        other_employer = self.create_test_employer(username="dave", password="davepass")
        position = self.create_test_position(employer, number_of_positions=1)

        application = create_application(student.id, position.id)
        assert application is not None

        # Non-existent application
        invalid_accept = accept_application(9999, employer.id)
        assert invalid_accept is None

        # Wrong employer
        invalid_accept = accept_application(application.id, other_employer.id)
        assert invalid_accept is None

        # No empty positions left
        position.number_of_positions = 0
        db.session.commit()

        invalid_accept = accept_application(application.id, employer.id)
        assert invalid_accept is None

    
    # Test rejecting a valid application
    def test_reject_application_valid(self):
        student = self.create_test_student()
        staff = self.create_test_staff()
        employer = self.create_test_employer()
        position = self.create_test_position(employer, number_of_positions=2)

        application = create_application(student.id, position.id)
        assert application is not None

        shortlisted = shortlist_application(application.id, staff.id)  
        assert shortlisted is not None

        rejected = reject_application(shortlisted.id, employer.id)
        assert rejected is not None
        assert rejected.state_name == "rejected"

        stored_application = get_application(shortlisted.id)
        assert stored_application.state_name == "rejected"