import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, open_position, add_student_to_shortlist, decide_shortlist, get_shortlist_by_student, get_shortlist_by_position, get_positions_by_employer)
from App.models.application import Application


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)
'''

def add_student_to_shortlist(student_id, position_id, staff_id):

    teacher = db.session.get(Staff, staff_id)
    student = db.session.get(Student, student_id)

    if not student or not teacher:
        return False

    existing = db.session.execute(
        db.select(Shortlist).filter_by(student_id=student.id, position_id=position_id)
    ).scalar_one_or_none()

    position = db.session.execute(
        db.select(Position)
        .filter(
            Position.id == position_id,
            Position.number_of_positions > 0,
            Position.status == "open"
        )
    ).scalar_one_or_none()

    if existing or not position:
        return False

    shortlist = Shortlist(
        student_id=student.id,
        position_id=position.id,
        staff_id=teacher.id,
        title=position.title
    )

    db.session.add(shortlist)
    db.session.commit()
    return shortlist


def decide_shortlist(student_id, position_id, decision):

    shortlist = db.session.execute(
        db.select(Shortlist)
        .filter_by(student_id=student_id, position_id=position_id, status="pending")
    ).scalar_one_or_none()

    position = db.session.get(Position, position_id)

    if not shortlist or not position or position.number_of_positions <= 0:
        return False

    shortlist.update_status(decision)
    position.update_number_of_positions(position.number_of_positions - 1)

    db.session.commit()
    return shortlist


def get_shortlist_by_student(student_id):
    return db.session.execute(
        db.select(Shortlist).filter_by(student_id=student_id)
    ).scalars().all()


def get_shortlist_by_position(position_id):
    return db.session.execute(
        db.select(Shortlist).filter_by(position_id=position_id)
    ).scalars().all()
'''
application_cli = AppGroup('application', help='Application object commands')

@application_cli.command("show", help="Shows application details")
@click.argument("application_id", type=int)
@with_appcontext
def show_application_command(application_id):
    """Show application details and current state."""
    application = Application.query.get(application_id)
    if not application:
        print(f'✗ Application with ID {application_id} not found')
        return

    print(f'\n📄 Application Details:')
    print(f'  ID: {application.id}')
    print(f'  Title: {application.title}')
    print(f'  Position ID: {application.position_id}')
    print(f'  Student ID: {application.student_id}')
    print(f'  Staff ID: {application.staff_id}')
    print(f'  State: {application.state_name}')
    print(f'  Can Accept: {application.can_user_accept()}')
    print(f'  Can Reject: {application.can_user_reject()}')
    print(f'  Can Shortlist: {application.can_user_shortlist()}')
    print(f'  Created: {application.created_at}')
   # print(f'  Updated: {application.updated_at}')

@application_cli.command("accept", help="Accept an internship application")
@click.argument("application_id", type=int)
@click.option("--user-id", type=int, help="User ID performing the action (must be employer)")
@with_appcontext
def accept_application_command(application_id, user_id):
    """Accept an application - transitions it to the accepted state."""
    application = Application.query.get(application_id)
    if not application:
        print(f'✗ Application with ID {application_id} not found')
        return

    user = None
    if user_id:
        user = User.query.get(user_id)
        if not user:
            print(f'✗ User with ID {user_id} not found')
            return

    try:
        old_state = application.state_name
        application.accept(user=user) 
        db.session.commit()

        user_info = f" by {user.username} ({user.role})" if user else ""
        print(f'✓ Application accepted{user_info}!')
        print(f'  Previous State: {old_state}')
        print(f'  Current State: {application.state_name}')

    except PermissionError as e:
        print(f'✗ Permission denied: {e}')
    except ValueError as e:
        print(f'✗ Cannot accept application: {e}')
    except Exception as e:
        db.session.rollback()
        print(f'✗ Error accepting application: {e}')
        


@application_cli.command("reject", help="Reject an internship application")
@click.argument("application_id", type=int)
@click.option("--user-id", type=int, help="User ID performing the action (must be employer)")
@with_appcontext
def reject_application_command(application_id, user_id):
    """Reject an application - transitions it to the rejected state."""
    application = Application.query.get(application_id)
    if not application:
        print(f'✗ Application with ID {application_id} not found')
        return

    user = None
    if user_id:
        user = User.query.get(user_id)
        if not user:
            print(f'✗ User with ID {user_id} not found')
            return

    try:
        old_state = application.state_name
        application.reject(user=user)  
        db.session.commit()

        user_info = f" by {user.username} ({user.role})" if user else ""
        print(f'✓ Application rejected{user_info}!')
        print(f'  Previous State: {old_state}')
        print(f'  Current State: {application.state_name}')

    except PermissionError as e:
        print(f'✗ Permission denied: {e}')
    except ValueError as e:
        print(f'✗ Cannot reject application: {e}')
    except Exception as e:
        db.session.rollback()
        print(f'✗ Error rejecting application: {e}')


@application_cli.command("shortlist", help="Shortlist an internship application")
@click.argument("application_id", type=int)
@click.option("--user-id", type=int, help="User ID performing the action (must be staff)")
@with_appcontext
def shortlist_application_command(application_id, user_id):
    """Shortlist an application - marks it as priority for review."""
    application = Application.query.get(application_id)
    if not application:
        print(f'✗ Application with ID {application_id} not found')
        return

    user = None
    if user_id:
        user = User.query.get(user_id)
        if not user:
            print(f'✗ User with ID {user_id} not found')
            return

    try:
        old_state = application.state_name
        application.shortlist(user=user) 
        db.session.commit()

        user_info = f" by {user.username} ({user.role})" if user else ""
        print(f'✓ Application shortlisted successfully{user_info}!')
        print(f'  Previous State: {old_state}')
        print(f'  Current State: {application.state_name}')
        print(f'  Application marked as priority for review')

    except PermissionError as e:
        print(f'✗ Permission denied: {e}')
    except ValueError as e:
        print(f'✗ Cannot shortlist application: {e}')
    except Exception as e:
        db.session.rollback()
        print(f'✗ Error shortlisting application: {e}')








@application_cli.command("list_all_applications", help="List all applications for a position")
@click.argument("position_id", type=int)
@with_appcontext
def list_applications_by_position_command(position_id):
    applications = Application.query.filter_by(position_id=position_id).all()
    
    if not applications:
        print(f'No applications found for this position')
        return
    
    print(f'\nApplications for Position {position_id}:')  
    for application in applications:
        print(f'Application ID: {application.id}')
        print(f'Title: {application.title}')
        print(f'Student ID: {application.student_id}')
        print(f'Shortlisting Staff ID: {application.staff_id}')
        print(f'State: {application.state_name}')
        print(f'Date Created: {application.created_at}')


@application_cli.command("demo", help="showcase application state transitions")
@click.argument("position-id", type=int, default=1)
@click.argument("student-id", type=int, default=1)
@click.argument("staff-id", type=int, default=1)
@with_appcontext
def demo_application_command(position_id, student_id, staff_id):
    try:
        application = Application(position_id=position_id, student_id=student_id, staff_id=staff_id, title="Demo Application"
        )
        db.session.add(application)
        db.session.commit()
        
        print(f"Demo Application created. Application ID: {application.id}")
        print(f"Initial State: {application.state_name}\n")
        
        print(f"Shortlist: {application.shortlist(staff_id)}\n")
        print(f"New State: {application.state_name}\n")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error in demo: {e}")


#app.cli.add_command(application_cli)


