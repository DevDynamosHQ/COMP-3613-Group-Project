from datetime import date
import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db

from App.models import User, Student, Staff

from App.controllers.user import create_user, get_user, get_user_by_username
from App.controllers.student import get_student
from App.controllers.staff import get_staff
from App.controllers.employer import get_employer

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


class UserControllerIntegrationTests(unittest.TestCase):

    # Tests that creating a user populates both the User table and role specific table
    def test_create_user_valid(self):
        student = create_user("hannah", "hannahpass", "student")
        staff = create_user("rick", "rickpass", "staff")
        employer = create_user("sam", "sampass", "employer")

        assert student is not None
        assert staff is not None
        assert employer is not None

        stored_student_user = get_user(student.id)
        stored_staff_user = get_user(staff.id)
        stored_employer_user = get_user(employer.id)

        assert stored_student_user is not None
        assert stored_staff_user is not None
        assert stored_employer_user is not None
       
        stored_student = get_student(student.id)
        stored_staff = get_staff(staff.id)
        stored_employer = get_employer(employer.id)
       
        assert stored_student is not None
        assert stored_student.username == "hannah"
        assert stored_student.role == "student"

        assert stored_staff is not None
        assert stored_staff.username == "rick"
        assert stored_staff.role == "staff"

        assert stored_employer is not None
        assert stored_employer.username == "sam"
        assert stored_employer.role == "employer"


     # Test to verify users with invalid roles cannot be created
    def test_create_user_invalid_role(self):
        invalid_user = create_user("bob", "bobpass", "invalid_role")
        assert invalid_user is False

        user_lookup = get_user_by_username("bob")
        assert user_lookup is None