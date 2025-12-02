from datetime import date
import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db

from App.models import User, Student, Staff

from App.controllers.user import create_user, get_user, get_user_by_username, get_all_users_json, update_user
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

    
    # Test to verify duplicate usernames are not created
    def test_create_user_duplicate_username(self):
        user1 = create_user("hannah", "pass123", "student")
        assert user1 is not None

        user2 = create_user("hannah", "differentpass", "student")
        assert user2 is False

        stored = get_user_by_username("hannah")
        assert stored is not None
        assert stored.id == user1.id  

    
    # Test to verify create user would not accept invalid input
    def test_create_user_invalid_inputs(self):
        # Empty username
        user_empty_username = create_user("", "pass123", "student")
        assert user_empty_username is False

        # No password
        user_no_password = create_user("no_pass", "", "student")
        assert user_no_password is False

        # None as role
        user_no_role = create_user("janet", "pass123", None)
        assert user_no_role is False

        # Spaces-only username
        user_spaces = create_user("    ", "pass123", "student")
        assert user_spaces is False

        # Very long username
        user_long = create_user("a" * 300, "pass123", "student")
        assert user_long is False

    
    # Tests get all users in JSON format
    def test_get_all_users_json(self):
        user1 = create_user("hannah", "hannahpass", "student")
        user2 = create_user("rick", "rickpass", "staff")
        user3 = create_user("sam", "sampass", "employer")

        assert user1 is not None
        assert user2 is not None
        assert user3 is not None

        users_json = get_all_users_json()

        expected_users = [
            {
                "id":user1.id, 
                "username":"hannah", 
                "role":"student", 
                "email":None, 
                "degree":None, 
                "phone":None,
                "gender":None,
                "gpa":None,
                "resume":None,
                "age":None
            }, 
            {
                "id":user2.id, 
                "username":"rick", 
                "role":"staff", 
                "email":None
            },
            {
                "id":user3.id, 
                "username":"sam", 
                "role":"employer", 
                "email":None, 
                "phone":None, 
                "company_name":None, 
                "positions":[]
            }
        ]
        
        self.assertListEqual(expected_users, users_json)

    
    # Test to verify user information is updated 
    def test_update_user(self):
        user = create_user("hannah", "hannahpass", "student")
        assert user is not None

        updated_user = update_user(user.id, username="hannah_new", password="newpass")
        assert updated_user is not None
        assert updated_user.username == "hannah_new"

        stored_user = get_user(user.id)
        assert stored_user.username == "hannah_new"
        assert stored_user.check_password("newpass")

    
    # Test that invalid user id cannot be updated
    def test_update_user_with_invalid_id(self):
        invalid_user = update_user(9999, username="hannah", password="hannahpass")
        assert invalid_user is None



