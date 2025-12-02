from datetime import date
import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db

from App.models import User, Student, Staff, Employer, Position

from App.controllers.user import create_user
from App.controllers.position import open_position, get_position, get_positions_by_employer, update_position



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


class PositionControllerIntegrationTests(unittest.TestCase):

    def create_test_employer1(self, username="sam"):
        employer = create_user(username, "pass123", "employer")
        assert employer is not None
        return employer
    
    def create_test_employer2(self, username="alex"):
        employer = create_user(username, "pass456", "employer")
        assert employer is not None
        return employer


    # Test to verify position is opened  
    def test_open_position(self):
        employer = self.create_test_employer1()

        position_count = 2
        description = "Entry-level IT support role."

        position = open_position(employer.id, "IT Support", position_count, description)
        
        assert position is not None

        stored_position = get_position(position.id)

        assert stored_position.title == "IT Support"
        assert stored_position.number_of_positions == position_count
        assert stored_position.description == description
        
    
    # Test to verify inavlid positions are not created
    def test_open_position_with_invalid_input(self):
        employer = self.create_test_employer1()

        invalid_employer_position = open_position(-1, "Developer", 1)
        assert invalid_employer_position is False

        negative_count_position = open_position(employer.id, "Developer", -1)
        assert negative_count_position is False

        zero_count_position = open_position(employer.id, "Developer", 0)
        assert zero_count_position is False

        empty_title_position = open_position(employer.id, "", 2)
        assert empty_title_position is False

    
     # Test to verify all positions by employer
    def test_get_positions_by_employer(self):
        employer = self.create_test_employer1()

        position1 = open_position(employer.id, "IT Support", 2)
        position2 = open_position(employer.id, "Developer", 1)

        assert position1 is not None
        assert position2 is not None

        positions = get_positions_by_employer(employer.id)
        assert len(positions) == 2
        assert all(p.employer_id == employer.id for p in positions)

    
    # Test to verify position is updated 
    def test_update_position(self):
        employer = self.create_test_employer1()

        position = open_position(employer.id, "Developer", 2, "Initial description")
        assert position is not None

        updated_position = update_position(position.id, employer.id, title="Senior Developer", description="Updated description", number_of_positions=3, status="open")
        assert updated_position is True

        stored_position = get_position(position.id)

        assert stored_position.title == "Senior Developer"
        assert stored_position.description == "Updated description"
        assert stored_position.number_of_positions == 3
        assert stored_position.status.value == "open"

    
    # Test to verify update position only accepts valid input
    def test_update_position_with_invalid_input(self):
        employer1 = self.create_test_employer1()

        employer2 = self.create_test_employer2()
        
        position = open_position(employer1.id, "Developer", 2)
        assert position is not None

        # Non-existent position ID
        result = update_position(9999, employer1.id, title="New Title")
        assert result is False

        # Correct position ID but wrong employer ID
        result = update_position(position.id, employer2.id, title="New Title")
        assert result is False

        # Invalid status
        result = update_position(position.id, employer1.id, status="invalid_status")
        assert result is False

        # Negative number of positions
        result = update_position(position.id, employer1.id, number_of_positions=-1)
        assert result is False

        # Zero number of positions
        result = update_position(position.id, employer1.id, number_of_positions=0)
        assert result is False

        # Empty title
        result = update_position(position.id, employer1.id, title="")
        assert result is False

