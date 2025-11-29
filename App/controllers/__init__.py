'''
from .user import *
from .auth import *
from .initialize import *
from .position import *
from .application import *
from .employer import *
from .staff import *
from .student import *

from flask import current_app as app
'''
from .application import application_cli

def register_commands(app):
    app.cli.add_command(application_cli)
