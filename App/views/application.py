from flask import Blueprint, jsonify, request
from App.database import db
from App.models.application import Application
from App.models.user import User

application_views = Blueprint('application_views', __name__)



@application_views.route('/applications', methods=['GET'])
def list_applications():
    applications = Application.query.all()
    return jsonify([app.to_dict() for app in applications]), 200


@application_views.route('/applications/<int:application_id>', methods=['GET'])
def get_application(application_id):
    application = Application.query.get(application_id)
    if not application:
        return jsonify({'error': 'Application not found'}), 404
    return jsonify(application.to_dict()), 200


@application_views.route('/applications', methods=['POST'])
def create_application():
    data = request.json

    required = ['position_id', 'student_id', 'staff_id', 'title']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        application = Application(
            position_id=data['position_id'],
            student_id=data['student_id'],
            staff_id=data['staff_id'],
            title=data['title']
        )
        db.session.add(application)
        db.session.commit()
        return jsonify({'message': 'Application created', 'application': application.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@application_views.route('/applications/<int:application_id>/accept', methods=['POST'])
def accept_application(application_id):
    application = Application.query.get(application_id)
    if not application:
        return jsonify({'error': 'Application not found'}), 404

    user_id = request.json.get("user_id")
    user = User.query.get(user_id) if user_id else None

    try:
        application.accept(user=user)
        db.session.commit()
        return jsonify({
            'message': 'Application accepted',
            'application': application.to_dict()
        }), 200

    except PermissionError as e:
        return jsonify({'error': str(e)}), 403

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@application_views.route('/applications/<int:application_id>/reject', methods=['POST'])
def reject_application(application_id):
    application = Application.query.get(application_id)
    if not application:
        return jsonify({'error': 'Application not found'}), 404

    user_id = request.json.get("user_id")
    user = User.query.get(user_id) if user_id else None

    try:
        application.reject(user=user)
        db.session.commit()
        return jsonify({
            'message': 'Application rejected',
            'application': application.to_dict()
        }), 200

    except PermissionError as e:
        return jsonify({'error': str(e)}), 403

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@application_views.route('/applications/<int:application_id>/shortlist', methods=['POST'])
def shortlist_application(application_id):
    application = Application.query.get(application_id)
    if not application:
        return jsonify({'error': 'Application not found'}), 404

    user_id = request.json.get("user_id")
    user = User.query.get(user_id) if user_id else None

    try:
        application.shortlist(user=user)
        db.session.commit()
        return jsonify({
            'message': 'Application shortlisted',
            'application': application.to_dict()
        }), 200

    except PermissionError as e:
        return jsonify({'error': str(e)}), 403

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400



'''
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from App.controllers import ( add_student_to_shortlist, decide_shortlist, get_shortlist_by_student, get_shortlist_by_position)


shortlist_views = Blueprint('shortlist_views', __name__)


@shortlist_views.route('/api/shortlist', methods = ['POST'])
@jwt_required()
def add_student_shortlist():
     if current_user.role != 'staff':
        return jsonify({"message": "Unauthorized user"}), 403
    
     data = request.json
     request_result = add_student_to_shortlist(student_id=data['student_id'], position_id=data['position_id'], staff_id=current_user.id)
     
     if request_result:
         return jsonify(request_result.toJSON()), 200
     else:
         return jsonify({"error": "Failed to add to shortlist"}), 401
     
     

@shortlist_views.route('/api/shortlist/student/<int:student_id>', methods = ['GET'])
@jwt_required()
def get_student_shortlist(student_id):
    
    if current_user.role == 'student' and current_user.id != student_id:
         return jsonify({"message": "Unauthorized user"}), 403
     
     
    shortlists = get_shortlist_by_student(student_id)
    
    return jsonify([s.toJSON() for s in shortlists]), 200
    


@shortlist_views.route('/api/shortlist',methods = ['PUT'] ) 
@jwt_required()
def shortlist_decide():
    if current_user.role != 'employer':
        return jsonify({"message": "Unauthorized user"}), 403
    
    
    data = request.json
    request_result = decide_shortlist(data['student_id'], data['position_id'], data['decision'])
   
    if request_result:
        return jsonify(request_result.toJSON()), 200
    else:
     return jsonify({"error": "Failed to update shortlist"}), 400
    

@shortlist_views.route('/api/shortlist/position/<int:position_id>', methods=['GET'])
@jwt_required()
def get_position_shortlist(position_id):
    if current_user.role != 'employer' and current_user.role != 'staff':
        return jsonify({"message": "Unauthorized user"}), 403
    
    
    shortlists = get_shortlist_by_position(position_id)
    return jsonify([s.toJSON() for s in shortlists]), 200 
     '''