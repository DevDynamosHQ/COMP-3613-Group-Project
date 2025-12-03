from datetime import datetime
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from datetime import date


from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_jwt_extended import jwt_required, current_user

from App.models import User, Student, Staff, Employer, Position, Application, PositionStatus
from App.controllers.position import get_all_open_positions, get_position
from App.controllers.user import get_user
from App.controllers.student import get_student, update_student
from App.controllers.application import create_application, get_applications_by_student, get_application

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/student/dashboard', methods=['GET', 'POST'])
@jwt_required()
def student_dashboard():

    if current_user.role != 'student':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    student = get_student(current_user.id)
    positions = get_all_open_positions()
    applications = get_applications_by_student(current_user.id)

    applied_position_ids = {app.position_id for app in applications}

    return render_template(
        'student_dashboard.html', 
        student=student,
        positions=positions,
        applications=applications,
        applied_position_ids=applied_position_ids,
        current_user=current_user,
        is_authenticated=True)


@student_views.route('/student/position/<int:position_id>', methods=['GET'])
@jwt_required()
def view_position(position_id):

    position = get_position(position_id)

    if not position:
        flash("Position not found", "error")
        return redirect(url_for("student_views.student_dashboard"))


    existing_application = Application.query.filter_by(
        student_id=current_user.id,
        position_id=position_id
    ).first()

    already_applied = existing_application is not None

    return render_template(
        "position_detail.html",
        position=position,
        current_user=current_user,
        already_applied=already_applied
    )



@student_views.route('/student/apply/<int:position_id>', methods=['POST'])
@jwt_required()
def apply_internship(position_id):
    if current_user.role != 'student':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    application = create_application(student_id=current_user.id, position_id=position_id)

    if application:
        flash("Application submitted successfully!", "success")
    else:
        flash("You already applied for this position or it is no longer available.", "error")

    return redirect(url_for("student_views.student_dashboard"))


@student_views.route('/student/application/<int:application_id>')
@jwt_required()
def view_application(application_id):

    if current_user.role != 'student':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    application = get_application(application_id)
    
    if not application or application.student_id != current_user.id:
        flash("Application not found", "error")
        return redirect(url_for("student_views.student_dashboard"))

    return render_template('view_application.html', application=application)


from datetime import date

@student_views.route('/student/profile', methods=['GET', 'POST'])
@jwt_required()
def student_profile():
    if current_user.role != 'student':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    student = get_student(current_user.id)

    
    student_age = None
    if student.dob:
        today = date.today()
        student_age = today.year - student.dob.year - ((today.month, today.day) < (student.dob.month, student.dob.day))

    if request.method == "POST":
        email = request.form.get("email")
        dob = request.form.get("dob")
        gender = request.form.get("gender")
        degree = request.form.get("degree")
        phone = request.form.get("phone")
        gpa = request.form.get("gpa")

       
        resume_file = request.files.get("resume")
        filename = None
        if resume_file and resume_file.filename.strip():
            filename = secure_filename(resume_file.filename)
            upload_path = os.path.join(current_app.static_folder, "uploads")
            Path(upload_path).mkdir(parents=True, exist_ok=True)
            resume_file.save(os.path.join(upload_path, filename))

        profile_file = request.files.get("profile_pic")
        profile_filename = None
        if profile_file and profile_file.filename.strip():
            profile_filename = secure_filename(profile_file.filename)
            upload_path = os.path.join(current_app.static_folder, "uploads")
            Path(upload_path).mkdir(parents=True, exist_ok=True)
            profile_file.save(os.path.join(upload_path, profile_filename))

        updated = update_student(
            student.id,
            email=email,
            dob=dob,
            gender=gender,
            degree=degree,
            phone=phone,
            gpa=gpa,
            resume=filename if filename else student.resume,
            profile_pic=profile_filename if profile_filename else student.profile_pic
        )

        if updated:
            flash("Profile updated successfully", "success")
        else:
            flash("Error updating profile", "danger")

        return redirect(url_for("student_views.student_profile"))

    return render_template('student_profile.html', student=student, student_age=student_age)
