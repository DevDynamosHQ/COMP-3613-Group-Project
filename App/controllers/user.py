from App.models import User, Student, Employer, Staff
from App.database import db

def create_user(username, password, role):
    if not username or username.strip() == "":
        print("Invalid username")
        return False
    
    if len(username) > 20:
        print("Username too long")
        return False
    
    if not password or password.strip() == "":
        print("Invalid password")
        return False
    
    if role not in ["student", "staff", "employer"]:
        print("Invalid role")
        return False
    
    try:
        existing = User.query.filter_by(username=username).first()

        if existing:
            print("Username already exists")
            return False
        
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


def get_user(user_id):
    return db.session.get(User, user_id)


def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()


def get_all_users():
    return db.session.scalars(db.select(User)).all()


def get_all_users_json():
    return [u.get_json() for u in get_all_users()]


def update_user(user_id, username=None, password=None):
    user = get_user(user_id)

    if not user:
        return None
    
    if username:
        user.username = username

    if password:
        user.set_password(password)
    
    try:
        db.session.add(user)
        return user
    
    except Exception as e:
        print(f"Error updating user: {e}")
        return None

