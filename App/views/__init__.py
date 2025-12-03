# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
#from .admin import setup_admin
from .student import student_views
from .staff import staff_views
from .employer import employer_views

from .position import position_views
from .application import application_views

'''
def add_views(app):
    app.register_blueprint(application_views)
'''

views = [user_views, index_views, auth_views, student_views, staff_views, employer_views, position_views, application_views] 
# blueprints must be added to this list