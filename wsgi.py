import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.models import User, Student, Employer, Staff, Position, Application

from App.controllers.initialize import initialize
from App.controllers.user import create_user, get_user, get_all_users, get_all_users_json
from App.controllers.position import get_all_open_positions, get_positions_by_employer, open_position, update_position
from App.controllers.application import (
    create_application,
    get_applications_by_student,
    shortlist_application,
    accept_application,
    reject_application,
    get_applications_by_position_and_state
)


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


# Command: flask user create <username> <password> <role>
# Example: flask user create rob robpass student


@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("role", default="student")
def create_user_command(username, password, role):
    result = create_user(username, password, role)
    if result:
        print(f'{username} created!')
    else:
        print("User creation failed")


# Command: flask user list [format]
# Example: flask user list string
    

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())


app.cli.add_command(user_cli) # add the group to the cli



student_cli = AppGroup('student', help='Student object commands') 

# Command: flask student view_open_positions
# Example: flask student view_open_positions


@student_cli.command("view_open_positions", help="Displays all positions")
def view_positions_command():
    positions = get_all_open_positions()

    if positions:
        for pos in positions:
            print(f'Position ID: {pos.id}')
            print(f'    Title: {pos.title}')
            print(f'    Description: {pos.description}')
            print(f'    Employer ID: {pos.employer_id}')
            print(f'    Number of slots: {pos.number_of_positions}')
            print(f'    Status: {pos.status}')
            print("\n\n__________________________________________________________________________\n\n")
    else:
        print("No positions available")
        print("\n\n__________________________________________________________________________\n\n")



# Command: flask student create_application <student_id> <position_id>
# Example: flask student create_application 1 3


@student_cli.command("create_application", help="Creates an application for a student to a position")
@click.argument("student_id", type=int)
@click.argument("position_id", type=int)
def create_application_command(student_id, position_id):
    
    application = create_application(student_id=student_id, position_id=position_id)
    if application:
        print(f"Application created successfully! Application ID: {application.id}")
        print(f"Student ID: {application.student_id}, Position ID: {application.position_id}, Status: {application.state_name}")
        print("\n\n__________________________________________________________________________\n\n")
    else:
        print("Failed to create application. Check if student and position IDs are valid.")
        print("\n\n__________________________________________________________________________\n\n")


# Command: flask student list_applications <student_id>
# Example: flask student list_applications 1
    

@student_cli.command("list_applications", help="List all applications for a student")
@click.argument("student_id", type=int)
def list_applications(student_id):
   
    applications = get_applications_by_student(student_id)
    
    if not applications:
        print(f"No applications found for student with ID {student_id}")
        return
    
  
    for app in applications:
        print(f"Application ID: {app.id}")
        print(f"Position ID: {app.position_id}")
        print(f"Staff ID: {app.staff_id}")
        print(f"State: {app.state_name}")
        print(f"Created At: {app.created_at}")
        print(f"Updated At: {app.updated_at}")
        print("-" * 50)


app.cli.add_command(student_cli) # add the group to the cli



staff_cli = AppGroup('staff', help='Staff object commands')


# Command: flask staff list_applied_applications <position_id> <state_name>
# Example: flask staff list_applied_applications 1 applied


@staff_cli.command("list_applied_applications", help="Lists all applied applications for a position")
@click.argument("position_id", type=int)
@click.argument("state_name", type=str) # e.g., applied, shortlisted, accepted, rejected
def list_applied_applications(position_id, state_name):
    applications = get_applications_by_position_and_state(position_id, state_name)
    if not applications:
        print(f"No applied applications found for position {position_id}")
        return
    
    print(f"Applied applications for position {position_id}:\n")
    for app in applications:
        print(f"Application ID: {app.id}, Student ID: {app.student_id}, State: {app.state_name}")
    print("\n______________________________________________________\n")


# Command: flask staff shortlist_application <application_id> <staff_id>
# Example: flask staff shortlist_application 1 5

@staff_cli.command("shortlist_application", help="Adds a student to a shortlist")
@click.argument("application_id", type=int)
@click.argument("staff_id", type=int)
def add_to_shortlist_command(application_id, staff_id):  

    result = shortlist_application(application_id, staff_id)
    
    if result:
        print(f'Application {application_id} has been added to the shortlist by staff {staff_id}.')
        print("\n\n__________________________________________________________________________\n\n")
    else:
        print('Failed to add to shortlist. Possible reasons:')
        print(f'    Application {application_id} does not exist')
        print('    Application already shortlisted')
        print(f'    Staff {staff_id} cannot shortlist this application')
        print("\n\n__________________________________________________________________________\n\n")


app.cli.add_command(staff_cli) # add the group to the cli




employer_cli = AppGroup('employer', help='Employer object commands')


# Command: flask employer view_positions <employer_id>
# Example: flask employer view_positions 3


@employer_cli.command("view_positions", help="Displays all positions")
@click.argument("employer_id")
def view_positions_command(employer_id):
    positions = get_positions_by_employer(employer_id)

    if positions:
        for pos in positions:
            print(f'Position ID: {pos.id}')
            print(f'    Title: {pos.title}')
            print(f'    Description: {pos.description}')
            print(f'    Employer ID: {pos.employer_id}')
            print(f'    Number of slots: {pos.number_of_positions}')
            print(f'    Status: {pos.status.value}')
            print("\n\n__________________________________________________________________________\n\n")
    else:
        print("No positions available")
        print("\n\n__________________________________________________________________________\n\n")


# Command: flask employer add_position <employer_id> <title> <number_of_positions>
# Example: flask employer add_position 3 "Software Engineer" 5


@employer_cli.command("add_position", help="Adds a position")
@click.argument("employer_id", default=1)
@click.argument("title", default="Software Engineer")
@click.argument("number_of_positions", default=1)
def add_position_command(employer_id, title, number_of_positions):
    position = open_position(employer_id, title, number_of_positions)
    if position:
        print(f'{title} created!')
    else:
        print(f'Employer {employer_id} does not exist')


# Command: flask employer update_position <position_id> <employer_id> [--title] [--number_of_positions] [--status]
# Example: flask employer update_position 4 3 --title "Senior Software Engineer" --number_of_positions 4 --status "closed"


@employer_cli.command("update_position", help="Updates a position")
@click.argument("position_id", type=int)
@click.argument("employer_id", type=int)
@click.option("--title", type=str, help="Title of the position")
@click.option("--number_of_positions", type=int, help="Number of slots")
@click.option("--status", type=click.Choice(["open", "closed"]), help="Status of the position")
def update_position_command(position_id, employer_id, title, number_of_positions, status):
    position = update_position(position_id=position_id, employer_id=employer_id, title=title, number_of_positions=number_of_positions, status=status)

    if position:
        print(f'Position {position_id} updated successfully!')
    else:
        print(f'Position {position_id} does not exist or update failed.')


# Command: flask employer list_shortlisted_applications <position_id> <state_name>
# Example: flask employer list_shortlisted_applications 2 shortlisted


@employer_cli.command("list_shortlisted_applications", help="Lists all shortlisted applications for a position")
@click.argument("position_id", type=int)
@click.argument("state_name", type=str)
def list_shortlisted_applications(position_id, state_name):
    applications = get_applications_by_position_and_state(position_id, state_name)
    if not applications:
        print(f"No shortlisted applications found for position {position_id}")
        return
    
    print(f"Shortlisted applications for position {position_id}:\n")
    for app in applications:
        print(f"Application ID: {app.id}, Student ID: {app.student_id}, State: {app.state_name}")
    print("\n______________________________________________________\n")


# Command: flask employer accept_application <application_id> <employer_id>
# Example: flask employer accept_application 2 3


@employer_cli.command("accept_application", help="Accepts an application for a position")
@click.argument("application_id", type=int)
@click.argument("employer_id", type=int, required=False)
def accept_application_command(application_id, employer_id=None):

    employer_user = get_user(employer_id) if employer_id else None
    application = accept_application(application_id, employer_id=employer_id)

    if application:
        print(f"Application {application_id} accepted successfully.")
        print("\n\n__________________________________________________________________________\n\n")
    else:
        print(f"Failed to accept application {application_id}.")
        print("\n\n__________________________________________________________________________\n\n")


# Command: flask employer reject_application <application_id> <employer_id>
# Example: flask employer reject_application 1 3


@employer_cli.command("reject_application", help="Rejects an application for a position")
@click.argument("application_id", type=int)
@click.argument("employer_id", type=int, required=False)
def reject_application_command(application_id, employer_id=None):

    employer_user = get_user(employer_id) if employer_id else None
    application = reject_application(application_id, employer_id=employer_id)

    if application:
        print(f"Application {application_id} rejected successfully.")
        print("\n\n__________________________________________________________________________\n\n")
    else:
        print(f"Failed to reject application {application_id}.")
        print("\n\n__________________________________________________________________________\n\n")


app.cli.add_command(employer_cli) # add the group to the cli



# Command to run all tests
# flask test user

# Command to run only unit tests
# flask test user unit

# Command to run only integration tests
# flask test user int


test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "unit"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "_integration"]))
    else:
        sys.exit(pytest.main(["-k", "test"]))
    

app.cli.add_command(test)