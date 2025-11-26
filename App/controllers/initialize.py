from App.database import db
from .user import create_user
from App.models import User, Student, Employer, Staff, Position, Application


def initialize():
    db.drop_all()
    db.create_all()

    print("Creating default users...")

    # Create users
    student1 = create_user("bob", "bobpass", role="student")
    student2 = create_user("alice", "alicepass", role="student")

    employer1 = create_user("frank", "frankpass", role="employer")

    staff1 = create_user("john", "johnpass", role="staff")
    staff2 = create_user("sara", "sarapass", role="staff")

    print(f"Students: {student1.username}, {student2.username}")
    print(f"Employer: {employer1.username}")
    print(f"Staff: {staff1.username}, {staff2.username}")

    # Create Positions
    print("\nCreating positions...")

    position1 = open_position(
        user_id=employer1.id,
        title="Software Engineer",
        number_of_positions=6
    )

    position2 = open_position(
        user_id=employer1.id,
        title="Mechanical Engineer",
        number_of_positions=6
    )

    print(f"✓ Created position: {position1.title}")
    print(f"✓ Created position: {position2.title}")


    # Create Applications in different states

    print("\nCreating applications in different states...")

    # 1. Application in APPLIED state
    app1 = Application(
        student_id=student1.student.id,
        position_id=position1.id,
        staff_id=staff1.staff.id,
        title="Bob - SWE Application"
    )
    db.session.add(app1)
    db.session.commit()
    print(f"✓ Application 1 created: '{app1.title}' (State: {app1.state_name})")

    # 2. Shortlisted application
    app2 = Application(
        student_id=student2.student.id,
        position_id=position1.id,
        staff_id=staff1.staff.id,
        title="Alice - SWE Application"
    )
    db.session.add(app2)
    db.session.commit()

    app2.shortlist(user=staff1)  # staff shortlists
    db.session.commit()
    print(f"✓ Application 2 created & shortlisted: '{app2.title}' (State: {app2.state_name})")

    # 3. Accepted application
    app3 = Application(
        student_id=student1.student.id,
        position_id=position2.id,
        staff_id=staff2.staff.id,
        title="Bob - ME Application"
    )
    db.session.add(app3)
    db.session.commit()

    app3.shortlist(user=staff2)
    app3.accept(user=staff2)
    db.session.commit()
    print(f"✓ Application 3 created, shortlisted, accepted: '{app3.title}' (State: {app3.state_name})")

    # 4. Rejected application
    app4 = Application(
        student_id=student2.student.id,
        position_id=position2.id,
        staff_id=staff2.staff.id,
        title="Alice - ME Application"
    )
    db.session.add(app4)
    db.session.commit()

    app4.shortlist(user=staff2)
    app4.reject(user=staff2)
    db.session.commit()
    print(f"✓ Application 4 created, shortlisted, rejected: '{app4.title}' (State: {app4.state_name})")

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
