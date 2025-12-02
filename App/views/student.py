from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from App.controllers.position import get_all_open_positions

student_views = Blueprint('user_views', __name__, template_folder='../templates')

@student_views.route('/dashboard')
@jwt_required()
def student_dashboard():

    if jwt_current_user.role != "student":
        flash("Unauthorized access.", "red")
        return redirect(url_for('auth_views.login_page'))  

    
    positions = get_all_open_positions()

    return render_template('student_dashboard.html', positions=positions)