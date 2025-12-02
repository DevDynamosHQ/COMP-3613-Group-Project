from flask import Blueprint, jsonify, request, flash, redirect, url_for, render_template
from flask_jwt_extended import jwt_required, current_user
#from App.controllers import (open_position, get_positions_by_employer, get_all_positions_json, get_positions_by_employer_json)

from App.controllers.position import (
    open_position,
    get_position,
    get_all_positions_json,
    get_positions_by_employer_json
)

position_views = Blueprint('position_views', __name__)

@position_views.route('/student/position/<int:position_id>', methods=['GET'])
@jwt_required()
def view_position(position_id):
   
    if current_user.role != 'student':
        flash("Unauthorized access", "error")
        return redirect(url_for("auth_views.login_page"))

   
    position = get_position(position_id)
    if not position:
        flash("Position not found", "error")
        return redirect(url_for("student_views.student_dashboard"))

    return render_template("position_detail.html", position=position)









#get all positions
@position_views.route('/api/positions/all', methods = ['GET'])
def get_all_positions():
    position_list = get_all_positions_json()
    return jsonify(position_list), 200

# for opening a position 
@position_views.route('/api/positions/create', methods = ['POST'])
@jwt_required()
def create_position():
     if current_user.role != 'employer':
        return jsonify({"message": "Unauthorized user"}), 403
    
     data = request.json
     position = open_position(title=data['title'], user_id=current_user.id, number_of_positions=data['number'])
     
     if position:
        return jsonify(position.toJSON()), 201
     else:
      return jsonify({"error": "Failed to create position"}), 400
  
  
# get positions for a given employer
@position_views.route('/api/employer/positions', methods=['GET'])
@jwt_required()
def get_employer_positions():
    
    if current_user.role != 'employer':
        return jsonify({"message": "Unauthorized user"}), 403
    
    return jsonify(get_positions_by_employer_json(current_user.id)), 200

