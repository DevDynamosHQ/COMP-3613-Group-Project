from datetime import datetime
from werkzeug.utils import secure_filename
import os

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_jwt_extended import jwt_required, current_user

from App.models import User, Student, Staff, Employer, Position, Application, PositionStatus
from App.controllers.position import get_all_open_positions, get_position
from App.controllers.user import get_user
from App.controllers import get_student

student_views = Blueprint('user_views', __name__, template_folder='../templates')

@student_views.route('/student/dashboard', methods=['GET', 'POST'])
@jwt_required()
def student_dashboard():

    if current_user.role != 'student':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    student = get_student(current_user.id)

    positions = get_all_open_positions()

    return render_template('student_dashboard.html', 
                           student=student,
                           positions=positions)
