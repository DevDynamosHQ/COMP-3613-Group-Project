from App.models import User, Student, Employer, Staff
from App.database import db

def create_user(username, password, role):
    try:
        if role not in ['student', 'employer', 'staff']:
            raise ValueError("Invalid role")
        
        if User.query.filter_by(username=username).first():
            return {"error": "Username already exists"}
        
        if role == "student":
            newuser = Student(username=username, password=password, role="student")
        elif role == "employer":
            newuser = Employer(username=username, password=password, role="employer")
        elif role == "staff":
            newuser = Staff(username=username, password=password, role="staff")
        else:
            return False
        
        db.session.add(newuser)
        db.session.commit()
        return newuser
    
    except Exception as e:
        db.session.rollback()
        print(f"Error creating user: {e}")
        return False


#edited
'''
def create_user(username, user_id, password, user_type):
    try:
        if user_type == "student":
            new_user = Student(username, user_id, password)
        elif user_type == "employer":
            new_user = Employer(username=username, password=password)
        elif user_type == "staff":
            new_user = Staff(username=username, password=password)

        db.session.add(new_user)
        db.session.commit()
        return new_user

    except Exception as e:
        db.session.rollback()
'''

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()


def get_user(id):
    return db.session.get(User, id)


def get_all_users():
    return db.session.scalars(db.select(User)).all()


def get_all_users_json():
    return [u.get_json() for u in get_all_users()]


def update_user(id, username=None, password=None):
    user = get_user(id)
    if not user:
        return None
    
    if username:
        user.username = username
    if password:
        user.set_password(password)

    db.session.commit()
    return user
