from datetime import datetime
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from datetime import date

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_jwt_extended import jwt_required, current_user

from App.controllers.application import get_applications_by_position_and_state
from App.controllers.student import get_student
from App.models import User, Student, Staff, Employer, Position, Application, PositionStatus
from App.controllers.employer import get_employer, update_employer
from App.controllers.user import get_user
from App.controllers.position import get_positions_by_employer, get_position, update_position

employer_views = Blueprint('employer_views', __name__, template_folder='../templates')

@employer_views.route('/employer/dashboard', methods=['GET', 'POST'])
@jwt_required()
def employer_dashboard():

    if current_user.role != 'employer':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    employer = get_employer(current_user.id)
    positions = get_positions_by_employer(current_user.id)
    shortlisted = [application for p in positions for application in get_applications_by_position_and_state(p.id, "shortlisted")]

    return render_template(
        'employer_dashboard.html',
        employer=employer,
        positions=positions,
        shortlisted=shortlisted,
        current_user=current_user,
        is_authenticated=True)

'''
@employer_views.route('/employer/edit/<int:position_id>', methods=['POST'])
@jwt_required()
def edit_position(position_id):
    if current_user.role != 'employer':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    employer = get_employer(current_user.id)

    title = request.form.get("title")
    description = request.form.get("description")
    number_of_positions = request.form.get("number_of_positions")
    status = request.form.get("status")

    try:
        number_of_positions = int(number_of_positions) if number_of_positions else None
    except ValueError:
        flash("Invalid number of positions.", "error")
        return redirect(url_for("employer_views.employer_dashboard"))

    success = update_position(
        position_id=position_id,
        employer_id=current_user.id,
        title=title,
        description=description,
        number_of_positions=number_of_positions,
        status=status
    )

    if success:
        flash("Position updated successfully!", "success")
    else:
        flash("Failed to update position. Check inputs or ownership.", "error")

    return redirect(url_for("employer_views.employer_dashboard"))


@employer_views.route('/employer/position/<int:position_id>', methods=['GET'])
@jwt_required()
def view_shortlisted_applications(position_id):

    position = get_applications_by_position_and_state(position_id, "shortlisted")

    if not position:
        flash("Position not found", "error")
        return redirect(url_for("employer_views.employer_dashboard"))
    return render_template(
        "position_detail.html",
        position=position,
        current_user=current_user,
    )
'''
@employer_views.route('/employer/profile', methods=['GET', 'POST'])
@jwt_required()
def employer_profile():
    if current_user.role != 'employer':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    employer = get_employer(current_user.id)

    if request.method == "POST":
        email = request.form.get("email")
        phone = request.form.get("phone")
        company = request.form.get("company")

        # --- Profile Picture Upload ---
        profile_file = request.files.get("profile_pic")
        profile_filename = None
        if profile_file and profile_file.filename.strip():
            profile_filename = secure_filename(profile_file.filename)
            upload_path = os.path.join(current_app.static_folder, "uploads")
            Path(upload_path).mkdir(parents=True, exist_ok=True)
            profile_file.save(os.path.join(upload_path, profile_filename))

        updated = update_employer(
            employer.id,
            email=email,
            phone=phone,
            company=company,
            profile_pic=profile_filename if profile_filename else employer.profile_pic
        )

        if updated:
            flash("Profile updated successfully", "success")
        else:
            flash("Error updating profile", "danger")

        return redirect(url_for("employer_views.employer_profile"))

    return render_template('employer_profile.html', employer=employer)