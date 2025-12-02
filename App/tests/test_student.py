from datetime import date
import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db

from App.models import User, Student

from App.controllers.user import create_user, get_user
from App.controllers.student import get_student, update_student, delete_student



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


class StudentControllerIntegrationTests(unittest.TestCase):

    def create_test_student(self, username="hannah", password="hannahpass"):
        student = create_user(username, password, "student")
        assert student is not None
        return student


    # Test to verify student information is updated in both Student and User tables
    def test_update_student(self):
        student = self.create_test_student()

        updated_student = update_student(
            student_id=student.id, 
            username="hannah_new",
            email="hannah@example.com",
            dob=date(2000, 1, 1),
            gender="female",
            degree="Computer Science",
            phone="123-456-7890",
            gpa=3.8,
            resume="Resume content here."
        )
        assert updated_student is True

        stored_student = get_student(student.id)
        
        assert stored_student.username == "hannah_new"
        assert stored_student.email == "hannah@example.com"
        assert stored_student.dob == date(2000, 1, 1)
        assert stored_student.gender == "female"
        assert stored_student.degree == "Computer Science"
        assert stored_student.phone == "123-456-7890"
        assert stored_student.gpa == 3.8
        assert stored_student.resume == "Resume content here."

        user_entry = get_user(student.id)
        assert user_entry.username == "hannah_new"

    
    # Test that verify invalid student id cannot be updated
    def test_update_student_with_invalid_id(self):
        invalid_student = update_student(
            student_id=9999,
            username="hannah_new",
            email="hannah@example.com",
            dob=date(2000, 1, 1),
            gender="female",
            degree="Computer Science",
            phone="123-456-7890",
            gpa=3.8,
            resume="Resume content here."
        )
        assert invalid_student is None

    
    # Test to verify student was deleted from both Student and User tables
    def test_delete_student(self):
        student = self.create_test_student()
        assert student is not None

        stored_student = get_student(student.id)
        assert stored_student is not None

        deleted_result = delete_student(student.id)
        assert deleted_result is True

        deleted_student = get_student(student.id)
        assert deleted_student is None

        user = get_user(student.id)
        assert user is None

    
    # Test that invalid student id cannot be deleted
    def test_delete_student_with_invalid_id(self):
        invalid_student = delete_student(9999) 
        assert invalid_student is False