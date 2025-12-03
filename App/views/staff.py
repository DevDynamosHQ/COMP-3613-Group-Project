from werkzeug.utils import secure_filename
import os
from pathlib import Path
from datetime import date


from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_jwt_extended import jwt_required, current_user

from App.models import User, Student, Staff, Employer, Position, Application, PositionStatus
from App.controllers.position import get_all_open_positions, get_position
from App.controllers.user import get_user
from App.controllers.staff import get_staff, update_staff
from App.controllers.application import get_applications_by_position, shortlist_application, get_application

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/staff/dashboard', methods=['GET', 'POST'])
@jwt_required()
def staff_dashboard():

    if current_user.role != 'staff':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

    staff = get_staff(current_user.id)
    positions = get_all_open_positions()

    return render_template(
        'staff_dashboard.html', 
        staff=staff,
        positions=positions,
        current_user=current_user,
        is_authenticated=True)

@staff_views.route('/staff/position/<int:position_id>', methods=['GET'])
@jwt_required()
def view_position_applications(position_id):

    position = get_position(position_id)

    if not position:
        flash("Position not found", "error")
        return redirect(url_for("staff_views.staff_dashboard"))

    return render_template(
        "position_detail.html",
        position=position,
        current_user=current_user,
    )

