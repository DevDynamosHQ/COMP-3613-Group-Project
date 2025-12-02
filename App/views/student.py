from datetime import datetime
from werkzeug.utils import secure_filename
import os

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_jwt_extended import jwt_required, current_user

from App.models import User, Student, Staff, Employer, Position, Application, PositionStatus
from App.controllers.position import get_all_open_positions, get_position
from App.controllers.user import get_user
from App.controllers.student import get_student
from App.controllers.application import create_application

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/student/dashboard', methods=['GET', 'POST'])
@jwt_required()
def student_dashboard():

    if current_user.role != 'student':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    student = get_student(current_user.id)
    positions = get_all_open_positions()

    return render_template(
        'student_dashboard.html', 
        student=student,
        positions=positions,
        current_user=current_user,
        is_authenticated=True)


@student_views.route('/student/apply/<int:position_id>', methods=['POST'])
@jwt_required()
def apply_internship(position_id):
    if current_user.role != 'student':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    success = create_application(student_id=current_user.id, position_id=position_id)

    if success:
        flash("Application submitted successfully!", "success")
    else:
        flash("Failed to apply — you may have already applied or the position is full.", "error")

    return redirect(url_for("student_views.student_dashboard"))
