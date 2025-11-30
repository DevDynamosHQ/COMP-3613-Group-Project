import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
#from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, open_position, add_student_to_shortlist, decide_shortlist, get_shortlist_by_student, get_shortlist_by_position, get_positions_by_employer)
from App.controllers import (
    create_user,
    get_all_users_json,
    get_all_users,
    initialize,
    open_position,
    get_positions_by_employer,
    create_new_position, 
    add_student_to_shortlist,
    get_all_positions,
    get_all_positions_json
)

from App.models.application import Application
#from App.controllers.application import application_cli as app_application_cli


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
#FIXED
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("user_id", default = 1)
@click.argument("password", default="robpass")
@click.argument("user_type", default="student")
def create_user_command(username, user_id, password, user_type):
    result = create_user(username, user_id, password, user_type)
    print(result.get_json())
    if hasattr(result, "user_id"):
        print(f'{username} created!')
    else:
        print("User creation failed")
# this command will be : flask user create bob bobpass

#TO FIX: Only outputs students!!
@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

#FIXED
@user_cli.command("add_position", help="Adds a position")
@click.argument("title", default="Software Engineer")
@click.argument("employer_id", default=101)
@click.argument("number", default=1)
@click.argument("position_id", default = 1)
def add_position_command(title, employer_id, number, position_id):
    position = create_new_position(employer_id, title, number, position_id)
    if position:
        print(f'{title} created!')
    else:
        print(f'Employer {employer_id} does not exist')

#CREATED
@user_cli.command("view_all_positions", help="View all positions")
@click.argument("format", default="string")
def view_all_positions_command(format):
    positions = get_all_positions()
    if format == 'string':
        print(positions)
    else:
        print(get_all_positions_json())

#TO DO: OPEN AND CLOSE POSITION COMMANDS


#TO FIX
@user_cli.command("add_to_shortlist", help="Adds a student to a shortlist")
@click.argument("student_id", default=1)
@click.argument("position_id", default=1)
@click.argument("staff_id", default=201)
def add_to_shortlist_command(student_id, position_id, staff_id):
    test = add_student_to_shortlist(student_id, position_id, staff_id)
    if hasattr(test, "position_id"):
        print(f'Student {student_id} added to shortlist for position {position_id}')
    else:
        print("Student could not be added to shortlist")

@user_cli.command("decide_shortlist", help="Decides on a shortlist")
@click.argument("student_id", default=1)
@click.argument("position_id", default=1)
@click.argument("decision", default="accepted")
def decide_shortlist_command(student_id, position_id, decision):
    test = decide_shortlist(student_id, position_id, decision)
    if test:
        print(f'Student {student_id} is {decision} for position {position_id}')
        print("\n\n__________________________________________________________________________\n\n")
    else:
        print(f'Student {student_id} not in shortlist for position {position_id}')
        print("\n\n__________________________________________________________________________\n\n")

@user_cli.command("get_shortlist", help="Gets a shortlist for a student")
@click.argument("student_id", default=1)
def get_shortlist_command(student_id):
    list = get_shortlist_by_student(student_id)
    if list:
        for item in list:
            print(f'Student {item.student_id} is {item.status.value} for position {item.position_id}')

        print("\n\n__________________________________________________________________________\n\n")
    else:
        print(f'Student {student_id} has no shortlists')
        print("\n\n__________________________________________________________________________\n\n")

@user_cli.command("get_shortlist_by_position", help="Gets a shortlist for a position")
@click.argument("position_id", default=1)
def get_shortlist_by_position_command(position_id):
    list = get_shortlist_by_position(position_id)
    if list:
        for item in list:
            print(f'Student {item.student_id} is {item.status.value} for {item.position.title} id: {item.position_id}')
            print(f'    Staff {item.staff_id} added this student to the shortlist')
            print(f'    Position {item.position_id} is {item.position.status.value}')
            print(f'    Position {item.position_id} has {item.position.number_of_positions} slots')
            print(f'    Position {item.position_id} is for {item.position.title}')
            print("\n\n__________________________________________________________________________\n\n")

    else:
        print(f'Position {position_id} has no shortlists')
        print("\n\n__________________________________________________________________________\n\n")

#CREATED
@user_cli.command("get_applied_by_position", help="Gets applications for a position")
@click.argument("position_id", default = 1)
def get_applied_by_position_command(position_id):
    list = Application.query.filter_by(position_id=position_id ).filter_by(state_name="applied").all()
    if list:
        for item in list:
            print(item)
    else:
        print(f'Position {position_id} has no shortlists')

@user_cli.command("get_positions_by_employer", help="Gets all positions for an employer")
@click.argument("employer_id", default=1)
def get_positions_by_employer_command(employer_id):
    list = get_positions_by_employer(employer_id)
    if list:
        for item in list:
            print(f'Position {item.id} is {item.status.value}')
            print(f'    Position {item.id} has {item.number_of_positions} slots')
            print(f'    Position {item.id} is for {item.title}')
            print("\n\n__________________________________________________________________________\n\n")
    else:
            print(f'Employer {employer_id} has no positions')
            print("\n\n__________________________________________________________________________\n\n")
            
app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)


'''
Application Commands - State Pattern Demo
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

    print(f'\nApplication Details:')
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
        print(f' Application accepted{user_info}!')
        print(f'  Previous State: {old_state}')
        print(f'  Current State: {application.state_name}')

    except PermissionError as e:
        print(f' Permission denied: {e}')
    except ValueError as e:
        print(f' Cannot accept application: {e}')
    except Exception as e:
        db.session.rollback()
        print(f' Error accepting application: {e}')
        


@application_cli.command("reject", help="Reject an internship application")
@click.argument("application_id", type=int)
@click.option("--user-id", type=int, help="User ID performing the action (must be employer)")
@with_appcontext
def reject_application_command(application_id, user_id):
    """Reject an application - transitions it to the rejected state."""
    application = Application.query.get(application_id)
    if not application:
        print(f' Application with ID {application_id} not found')
        return

    user = None
    if user_id:
        user = User.query.get(user_id)
        if not user:
            print(f' User with ID {user_id} not found')
            return

    try:
        old_state = application.state_name
        application.reject(user=user)  
        db.session.commit()

        user_info = f" by {user.username} ({user.role})" if user else ""
        print(f' Application rejected{user_info}!')
        print(f'  Previous State: {old_state}')
        print(f'  Current State: {application.state_name}')

    except PermissionError as e:
        print(f' Permission denied: {e}')
    except ValueError as e:
        print(f' Cannot reject application: {e}')
    except Exception as e:
        db.session.rollback()
        print(f' Error rejecting application: {e}')


@application_cli.command("shortlist", help="Shortlist an internship application")
@click.argument("application_id", type=int)
@click.option("--user-id", type=int, help="User ID performing the action (must be staff)")
@with_appcontext
def shortlist_application_command(application_id, user_id):
    """Shortlist an application - marks it as priority for review."""
    application = Application.query.get(application_id)
    if not application:
        print(f' Application with ID {application_id} not found')
        return

    user = None
    if user_id:
        user = User.query.get(user_id)
        if not user:
            print(f' User with ID {user_id} not found')
            return

    try:
        old_state = application.state_name
        application.shortlist(user=user) 
        db.session.commit()

        user_info = f" by {user.username} ({user.role})" if user else ""
        print(f' Application shortlisted successfully{user_info}!')
        print(f'  Previous State: {old_state}')
        print(f'  Current State: {application.state_name}')
        print(f'  Application marked as priority for review')

    except PermissionError as e:
        print(f' Permission denied: {e}')
    except ValueError as e:
        print(f' Cannot shortlist application: {e}')
    except Exception as e:
        db.session.rollback()
        print(f' Error shortlisting application: {e}')








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


app.cli.add_command(application_cli)