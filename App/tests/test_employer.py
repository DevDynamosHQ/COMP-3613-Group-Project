from datetime import date
import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash


from App.main import create_app
from App.database import db, create_db

from App.models import User, Student, Staff, Employer

from App.controllers.user import create_user, get_user
from App.controllers.employer import get_employer, update_employer


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


class EmployerControllerIntegrationTests(unittest.TestCase):

    def create_test_employer(self, username="sam", password="sampass"):
        employer = create_user(username, password, "employer")
        assert employer is not None
        return employer


    # Test to verify employer information is updated in both Employer and User tables
    def test_update_employer(self):
        employer = self.create_test_employer()

        updated_employer = update_employer(employer.id, username="sam_new", company_name="New Company", email="newemail@example.com")
        assert updated_employer is True

        stored_employer = get_employer(employer.id)
        assert stored_employer.username == "sam_new"
        assert stored_employer.company_name == "New Company"
        assert stored_employer.email == "newemail@example.com"

        user_entry = get_user(employer.id)
        assert user_entry.username == "sam_new"


    # Test that verify invalid employer id cannot be updated
    def test_update_employer_with_invalid_id(self):
        invalid_employer = update_employer(9999, username="sam_new", company_name="New Company", email="sam@example.com")
        assert invalid_employer is False
