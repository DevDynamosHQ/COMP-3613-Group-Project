from datetime import datetime
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from datetime import date

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_jwt_extended import jwt_required, current_user

from App.controllers.application import accept_application, get_application, get_applications_by_position_and_state, reject_application
from App.controllers.student import get_student
from App.models import User, Student, Staff, Employer, Position, Application, PositionStatus
from App.controllers.employer import get_employer, update_employer
from App.controllers.user import get_user
from App.controllers.position import get_positions_by_employer, get_position, update_position

employer_views = Blueprint('employer_views', __name__, template_folder='../templates')

@employer_views.route('/employer/dashboard', methods=['GET'])
@jwt_required()
def employer_dashboard():
    if current_user.role != 'employer':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    employer = get_employer(current_user.id)
    positions = get_positions_by_employer(current_user.id)

    selected_position_id = request.args.get("selected_position", type=int)
    shortlisted = []

    q_positions = request.args.get("q_positions", "").lower()
    if q_positions:
        positions = [pos for pos in positions if q_positions in pos.title.lower()]

    if selected_position_id:
        shortlisted = get_applications_by_position_and_state(selected_position_id, "shortlisted")

    return render_template(
        'employer_dashboard.html',
        employer=employer,
        positions=positions,
        shortlisted=shortlisted,
        selected_position=selected_position_id,
        current_user=current_user,
        is_authenticated=True,
        q_positions=request.args.get("q_positions", "")
    )



@employer_views.route('/employer/edit/<int:position_id>', methods=['GET', 'POST'])
@jwt_required()
def edit_position(position_id):
    if current_user.role != 'employer':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    position = get_position(position_id)
    if not position or position.employer_id != current_user.id:
        flash("Position not found or unauthorized", "error")
        return redirect(url_for('employer_views.employer_dashboard'))

    if request.method == 'POST':
        # Update the position
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
            flash("Failed to update position.", "error")
        return redirect(url_for('employer_views.employer_dashboard'))

    # GET request: render edit form
    return render_template('edit_position.html', position=position)



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

@employer_views.route('/employer/create', methods=['GET', 'POST'])
@jwt_required()
def create_position():
    if current_user.role != 'employer':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    employer = get_employer(current_user.id)

    if request.method == 'POST':
        title = request.form.get("title")
        description = request.form.get("description")
        number_of_positions = request.form.get("number_of_positions")
        status = request.form.get("status")

        try:
            number_of_positions = int(number_of_positions) if number_of_positions else None
        except ValueError:
            flash("Invalid number of positions.", "error")
            return redirect(url_for("employer_views.create_position"))

        new_position = Position(
            title=title,
            description=description,
            number_of_positions=number_of_positions,
            status=PositionStatus[status.lower()] if status else PositionStatus.open,
            employer_id=current_user.id
        )

        from App.database import db
        try:
            db.session.add(new_position)
            db.session.commit()
            flash("Position created successfully!", "success")
            return redirect(url_for("employer_views.employer_dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"Failed to create position: {str(e)}", "error")
            return redirect(url_for("employer_views.create_position"))

    return render_template("create_position.html", current_user=current_user)


@employer_views.route('/employer/application/<int:position_id>/<int:application_id>')
@jwt_required()
def review_shortlist_application(position_id, application_id):
    if current_user.role != 'employer':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    application = get_application(application_id)
    
    if not application or application.position_id != position_id:
        flash("Application not found", "error")
        return redirect(url_for("employer_views.employer_dashboard"))

    if application.position.employer_id != current_user.id:
        flash("You are not authorized to view this application.", "error")
        return redirect(url_for("employer_views.employer_dashboard"))

    return render_template(
        'review_shortlist_student.html',
        application=application,
        current_user=current_user
    )

# Accept a shortlisted student
@employer_views.route('/employer/application/<int:application_id>/accept', methods=['POST'])
@jwt_required()
def accept_shortlist_application(application_id):
    if current_user.role != 'employer':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    application = get_application(application_id)
    if not application:
        flash("Application not found", "error")
        return redirect(url_for("employer_views.employer_dashboard"))

    try:
        accept_application(application_id, current_user.id)
        flash(f"{application.student.username} has been accepted.", "success")
    except Exception as e:
        flash(f"Failed to accept application: {str(e)}", "error")

    return redirect(url_for("employer_views.employer_dashboard", selected_position=application.position_id))

# Reject a shortlisted student
@employer_views.route('/employer/application/<int:application_id>/reject', methods=['POST'])
@jwt_required()
def reject_shortlist_application(application_id):
    if current_user.role != 'employer':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    application = get_application(application_id)
    if not application:
        flash("Application not found", "error")
        return redirect(url_for("employer_views.employer_dashboard"))

    try:
        reject_application(application_id, current_user.id)
        flash(f"{application.student.username} has been rejected.", "success")
    except Exception as e:
        flash(f"Failed to reject application: {str(e)}", "error")

    return redirect(url_for("employer_views.employer_dashboard", selected_position=application.position_id))

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
        company_name= request.form.get("company")

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
            company_name=company_name,
            profile_pic=profile_filename if profile_filename else employer.profile_pic
        )

        if updated:
            flash("Profile updated successfully", "success")
        else:
            flash("Error updating profile", "danger")

        return redirect(url_for("employer_views.employer_profile"))

    return render_template('employer_profile.html', employer=employer)