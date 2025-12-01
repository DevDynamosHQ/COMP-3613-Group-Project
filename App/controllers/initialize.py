from App.database import db
from App.models import *
from App.controllers import create_user
from App.controllers.application import create_application, reject_application, shortlist_application, accept_application
from App.controllers.position import open_position


def initialize():
    db.drop_all()
    db.create_all()

    print("Creating default users...")

    # Create users - these will return User objects with auto-generated IDs
    student1 = create_user('bob', 'bobpass', "student")
    student2 = create_user('gary', 'garypass', "student")

    employer1 = create_user('frank', 'frankpass', "employer")
    employer2 = create_user('rob', 'robpass', "employer")

    staff1 = create_user('john', 'johnpass', "staff")
    staff2 = create_user('sara', 'sarapass', "staff")


    print(f"Students: {student1.username} (ID: {student1.id}), {student2.username} (ID: {student2.id})")
    print(f"Employers: {employer1.username} (ID: {employer1.id}), {employer2.username} (ID: {employer2.id})")
    print(f"Staff: {staff1.username} (ID: {staff1.id}), {staff2.username} (ID: {staff2.id})")
    

    # Create Positions
    print("\nCreating positions...")

    # # Use the actual id from the employer object, not user_id
    position1 = open_position(employer_id=employer1.id, title='Software Engineer', number_of_positions= 6, description='Develop and maintain software applications.')
    position2 = open_position(employer_id=employer1.id, title='Mechanical Engineer', number_of_positions= 6, description='Design and develop mechanical systems.')
    position3 = open_position(employer_id=employer2.id, title='Software Engineer', number_of_positions= 6, description='Develop and maintain software applications.')

    print(f"Created position: {position1.title}")
    print(f"Created position: {position2.title}")
    print(f"Created position: {position3.title}")

    
    # Create Applications in different states
    print("\nCreating applications in different states...")

    application1 = create_application(student_id=student1.id, position_id=1)
    application2 = create_application(student_id=student1.id, position_id=2)

    application3 = create_application(student_id=student2.id, position_id=1)
    application4 = create_application(student_id=student2.id, position_id=2)

    print(f"Application 1 created: Application ID: {application1.id} (State: {application1.state_name})")
    print(f"Application 2 created: Application ID: {application2.id} (State: {application2.state_name})")
    print(f"Application 3 created: Application ID: {application3.id} (State: {application3.state_name})")
    print(f"Application 4 created: Application ID: {application4.id} (State: {application4.state_name})")

    shortlist_application(application_id=2, staff_id=staff1.id)
    shortlist_application(application_id=3, staff_id=staff2.id)
    shortlist_application(application_id=4, staff_id=staff2.id)

    accept_application(application_id=3, employer_id=employer1.id)
    reject_application(application_id=4, employer_id=employer1.id)

    print("\nUpdated application states...")
    print(f"Application 1 still in applied state: Application ID: {application1.id} (State: {application1.state_name})")
    print(f"Application 2 shortlisted: Application ID: {application2.id} (State: {application2.state_name})")
    print(f"Application 3 shortlisted and accepted: Application ID: {application3.id} (State: {application3.state_name})")
    print(f"Application 4 shortlisted and rejected: Application ID: {application4.id} (State: {application4.state_name})")

    # Summary
    print("\n" + "="*60)
    print("Summary:")
    print("="*60)

    print(f"Users created: {User.query.count()}")
    print(f"Positions created: {Position.query.count()}")
    print(f"Applications created: {Application.query.count()}")

    print("\nApplications by state:")
    state_counts = (
        db.session.query(Application.state_name, db.func.count(Application.id))
        .group_by(Application.state_name)
        .all()
    )
    for state, count in state_counts:
        print(f"  {state}: {count}")

    print("\nApplications per position:")
    for pos in Position.query.all():
        print(f"  Employer ID: {pos.employer_id}, Position Title:{pos.title}: {len(pos.applications)} applications")

    print("="*60)
