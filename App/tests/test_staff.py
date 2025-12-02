from datetime import date
import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db

from App.models import User, Student, Staff

from App.controllers.user import create_user, get_user
from App.controllers.staff import get_staff, update_staff, delete_staff


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


class StaffControllerIntegrationTests(unittest.TestCase):

    def create_test_staff(self, username="rick", password="rickpass"):
        staff = create_user(username, password, "staff")
        assert staff is not None
        return staff


    # Test to verify staff information is updated in both Staff and User tables
    def test_update_staff(self):
        staff = self.create_test_staff()

        updated_staff = update_staff(staff.id, username="rick_new", email="rick_new@example.com")
        assert updated_staff is True

        stored_staff = get_staff(staff.id)
        assert stored_staff.username == "rick_new"
        assert stored_staff.email == "rick_new@example.com"

        user_entry = get_user(staff.id)
        assert user_entry.username == "rick_new"

    
    # Test that verify invalid staff id cannot be updated
    def test_update_staff_with_invalid_id(self):
        invalid_staff = update_staff(9999, username="rick_new", email="rick@example.com")
        assert invalid_staff is None

    
    # Test to verify staff was deleted from both Staff and User tables
    def test_delete_staff(self):
        staff = self.create_test_staff()

        stored_staff = get_staff(staff.id)
        assert stored_staff is not None

        deleted_result = delete_staff(staff.id)
        assert deleted_result is True

        deleted_staff = get_staff(staff.id)
        assert deleted_staff is None

        user = get_user(staff.id)
        assert user is None