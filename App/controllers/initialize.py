from App.database import db
from App.models import *
from App.controllers import create_user
from App.controllers.application import create_application, shortlist_application
from App.controllers.position import open_position




def initialize():
    db.drop_all()
    db.create_all()

    bob = create_user('bob', 'bobpass', "student")
    frank = create_user('frank', 'frankpass', "employer")
    john = create_user('john', 'johnpass', "staff")

    rob = create_user('rob', 'robpass', "employer")

    open_position(employer_id=frank.id, title='Software Engineer', number_of_positions= 6, description='Develop and maintain software applications.')
    open_position(employer_id=frank.id, title='Mechanical Engineer', number_of_positions= 6, description='Design and develop mechanical systems.')
    open_position(employer_id=rob.id, title='Software Engineer', number_of_positions= 6, description='Develop and maintain software applications.')
    
    create_application(student_id=bob.id, position_id=1)
    create_application(student_id=bob.id, position_id=2)
    shortlist_application(application_id=1, staff_id=john.id)



    # print("Creating default users...")

    # # Create users - these will return User objects with auto-generated IDs
    # student1 = create_student("bob", "bobpass")
    # student2 = create_student("alice", "alicepass")

    # employer1 = create_employer("frank", "frankpass")

    # staff1 = create_staff("john", "johnpass")
    # staff2 = create_staff("sara", "sarapass")

    # # Commit to get the IDs
    # db.session.commit()

    # print(f"Students: {student1.username} (ID: {student1.id}), {student2.username} (ID: {student2.id})")
    # print(f"Employer: {employer1.username} (ID: {employer1.id})")
    # print(f"Staff: {staff1.username} (ID: {staff1.id}), {staff2.username} (ID: {staff2.id})")

    # # Create Positions
    # print("\nCreating positions...")

    # # Use the actual id from the employer object, not user_id
    # position1 = create_new_position(employer1.id, "Software Engineer", 6, 1)
    # position2 = create_new_position(employer1.id, "Mechanical Engineer", 6, 2)

    # db.session.commit()

    # print(f"Created position: {position1.title}")
    # print(f"Created position: {position2.title}")

    # # Create Applications in different states
    # print("\nCreating applications in different states...")

    # # 1. Application in APPLIED state
    # app1 = Application(
    #     student_id=student1.id,  # Use id, not user_id
    #     position_id=position1.id,
    #     staff_id=staff1.id,      # Use id, not user_id
    #     title="Bob - SWE Application"
    # )
    # db.session.add(app1)
    # db.session.commit()
    # print(f"Application 1 created: '{app1.title}' (State: {app1.state_name})")

    # # 2. Shortlisted application
    # app2 = Application(
    #     student_id=student2.id,  # Use id, not user_id
    #     position_id=position1.id,
    #     staff_id=staff1.id,      # Use id, not user_id
    #     title="Alice - SWE Application"
    # )
    # db.session.add(app2)
    # db.session.commit()

    # app2.shortlist(user=staff1)  # staff shortlists
    # db.session.commit()
    # print(f"Application 2 created & shortlisted: '{app2.title}' (State: {app2.state_name})")

    # # 3. Accepted application
    # app3 = Application(
    #     student_id=student1.id,  # Use id, not user_id
    #     position_id=position2.id,
    #     staff_id=staff2.id,      # Use id, not user_id
    #     title="Bob - ME Application"
    # )
    # db.session.add(app3)
    # db.session.commit()

    # app3.shortlist(user=staff2)
    # app3.accept(user=employer1)
    # db.session.commit()
    # print(f"Application 3 created, shortlisted, accepted: '{app3.title}' (State: {app3.state_name})")

    # # 4. Rejected application
    # app4 = Application(
    #     student_id=student2.id,  # Use id, not user_id
    #     position_id=position2.id,
    #     staff_id=staff2.id,      # Use id, not user_id
    #     title="Alice - ME Application"
    # )
    # db.session.add(app4)
    # db.session.commit()

    # app4.shortlist(user=staff2)
    # app4.reject(user=employer1)
    # db.session.commit()
    # print(f"Application 4 created, shortlisted, rejected: '{app4.title}' (State: {app4.state_name})")

    # # Summary
    # print("\n" + "="*60)
    # print("Summary:")
    # print("="*60)

    # print(f"Users created: {User.query.count()}")
    # print(f"Positions created: {Position.query.count()}")
    # print(f"Applications created: {Application.query.count()}")

    # print("\nApplications by state:")
    # state_counts = (
    #     db.session.query(Application.state_name, db.func.count(Application.id))
    #     .group_by(Application.state_name)
    #     .all()
    # )
    # for state, count in state_counts:
    #     print(f"  {state}: {count}")

    # print("\nApplications per position:")
    # for pos in Position.query.all():
    #     print(f"  {pos.title}: {len(pos.applications)} applications")

    # print("="*60)

'''
from App.controllers.position import open_position
from App.database import db
from .student import create_student
from .employer import create_employer
from .staff import create_staff
from .position import create_new_position
from App.models import User, Student, Employer, Staff, Position, Application


def initialize():
    db.drop_all()
    db.create_all()

    print("Creating default users...")

    # Create users
    student1 = create_student("bob", "bobpass")
    student2 = create_student("alice", "alicepass")

    employer1 = create_employer("frank", "frankpass")

    staff1 = create_staff("john", "johnpass")
    staff2 = create_staff("sara", "sarapass")

    print(f"Students: {student1.username}, {student2.username}")
    print(f"Employer: {employer1.username}")
    print(f"Staff: {staff1.username}, {staff2.username}")

    # Create Positions
    print("\nCreating positions...")

    position1 = create_new_position(employer1.user_id, "Software Engineer", 6, 1,)

    position2 = create_new_position(employer1.user_id, "Mechanical Engineer", 6, 2)

    print(f"Created position: {position1.title}")
    print(f"Created position: {position2.title}")


    # Create Applications in different states

    print("\nCreating applications in different states...")

    # 1. Application in APPLIED state
    app1 = Application(
        student_id=student1.user_id,
        position_id=position1.id,
        staff_id=staff1.user_id,
        title="Bob - SWE Application"
    )
    db.session.add(app1)
    db.session.commit()
    print(f"Application 1 created: '{app1.title}' (State: {app1.state_name})")

    # 2. Shortlisted application
    app2 = Application(
        student_id=student2.user_id,
        position_id=position1.id,
        staff_id=staff1.user_id,
        title="Alice - SWE Application"
    )
    db.session.add(app2)
    db.session.commit()

    app2.shortlist(user=staff1)  # staff shortlists
    db.session.commit()
    print(f"Application 2 created & shortlisted: '{app2.title}' (State: {app2.state_name})")

    # 3. Accepted application
    app3 = Application(
        student_id=student1.user_id,
        position_id=position2.id,
        staff_id=staff2.user_id,
        title="Bob - ME Application"
    )
    db.session.add(app3)
    db.session.commit()

    app3.shortlist(user=staff2)
    app3.accept(user=employer1)
    db.session.commit()
    print(f"Application 3 created, shortlisted, accepted: '{app3.title}' (State: {app3.state_name})")

    # 4. Rejected application
    app4 = Application(
        student_id=student2.user_id,
        position_id=position2.id,
        staff_id=staff2.user_id,
        title="Alice - ME Application"
    )
    db.session.add(app4)
    db.session.commit()

    app4.shortlist(user=staff2)
    app4.reject(user=employer1)
    db.session.commit()
    print(f"Application 4 created, shortlisted, rejected: '{app4.title}' (State: {app4.state_name})")

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
        print(f"  {pos.title}: {len(pos.applications)} applications")

    print("="*60)

'''