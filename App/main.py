import os
from flask import Flask, render_template
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS

from App.database import init_db
from App.config import load_config
from App.controllers import setup_jwt, add_auth_context


def register_blueprints(app):
    

    from App.views.user import user_views
    from App.views.index import index_views
    from App.views.auth import auth_views
    from App.views.student import student_views
    from App.views.staff import staff_views
    from App.views.position import position_views
    from App.views.application import application_views
    from App.views.employer import employer_views


    app.register_blueprint(user_views)
    app.register_blueprint(index_views)
    app.register_blueprint(auth_views)
    app.register_blueprint(student_views)
    app.register_blueprint(staff_views)
    app.register_blueprint(position_views)
    app.register_blueprint(application_views)
    app.register_blueprint(employer_views)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')

    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)

    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)

    register_blueprints(app)

    init_db(app)

    jwt = setup_jwt(app)

    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401

    return app



'''
import os
from flask import Flask, render_template
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from App.database import init_db
from App.config import load_config


from App.controllers import (
    setup_jwt,
    add_auth_context
)

from App.views import views #setup_admin



def add_views(app):
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    jwt = setup_jwt(app)
    #setup_admin(app)
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401
    app.app_context().push()
    return app
'''