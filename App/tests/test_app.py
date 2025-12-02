import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Employer, Position, Application, Staff, Student, PositionStatus


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
# class UserUnitTests(unittest.TestCase):

#     def test_new_user(self):
#         user = User("bob", "bobpass")
#         assert user.username == "bob"

#     def test_new_student(self):
#             student = Student("john", "johnpass")
#             assert student.username == "john"
#             assert student.role == "student"

#     def test_new_staff(self):
#         staff = Staff("jim", "jimpass")
#         assert staff.username == "jim"
#         assert staff.role == "staff"

#     def test_new_employer(self):
#         employer = Employer("alice", "alicepass")
#         assert employer.username == "alice"
#         assert employer.role == "employer"

#     def test_new_position(self):
#         position = Position("Software Developer", 10, 5) 
#         assert position.title == "Software Developer"
#         assert position.employer_id == 10
#         assert position.status == "open"
#         assert position.number_of_positions == 5

#     def test_new_shortlist(self):
#         shortlist = Shortlist(1,2,3)
#         assert shortlist.student_id == 1
#         assert shortlist.position_id == 2
#         assert shortlist.staff_id == 3
#         assert shortlist.status == "pending"

#     # pure function no side effects or integrations called
#     def test_get_json(self):
#         user = User("bob", "bobpass")
#         user_json = user.get_json()
#         self.assertEqual(user_json["username"], "bob")
#         self.assertTrue("id" in user.get_json())
    
#     def test_hashed_password(self):
#         password = "mypass"
#         hashed = generate_password_hash(password)
#         user = User("bob", password)
#         assert user.password != password

#     def test_check_password(self):
#         password = "mypass"
#         user = User("bob", password)
#         assert user.check_password(password)
