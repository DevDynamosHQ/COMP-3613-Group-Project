from flask import (
    Blueprint, render_template, jsonify,
    request, flash, redirect, url_for, make_response
)
from flask_jwt_extended import (
    jwt_required, current_user,
    unset_jwt_cookies, set_access_cookies
)

from App.controllers.auth import login
from App.controllers.user import create_user, get_user_by_username

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')



@auth_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@auth_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')


@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template(
        'message.html',
        title="Identify",
        message=f"You are logged in as {current_user.id} - {current_user.username}"
    )


@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data.get('username'), data.get('password'))

    
    if not token:
        flash("Invalid username or password", "error")
        return redirect(request.referrer)

    flash("Login Successful", "success")

    user = get_user_by_username(data.get('username'))
    if user.role == 'student':
        response = redirect(url_for('student_views.student_dashboard'))
    elif user.role == 'staff':
        response = redirect(url_for('staff_views.staff_dashboard'))
    elif user.role == 'employer':
        response = redirect(url_for('employer_views.employer_dashboard'))
    else:
        response = redirect(url_for('index_views.index_page'))

    set_access_cookies(response, token)
    return response


@auth_views.route('/signup', methods=['POST'])
def signup_action():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')  

    created = create_user(username, password, role )
    #response = redirect(url_for('index_views.index'))
    response = redirect(url_for('index_views.index_page'))
    if not created:
        flash("Signup failed — username already taken", "error")
        return redirect(request.referrer)

    
    token = login(username, password)
    flash("Signup Successful", "success")
    set_access_cookies(response, token)
    return response


@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = make_response(render_template('logout.html'))
    unset_jwt_cookies(response)
    return response

'''
@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for('index_views.index'))
    flash("Logged Out", "info")
    unset_jwt_cookies(response)
    return response

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for('index_views.index_page'))
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response
'''


@auth_views.route('/api/login', methods=['POST'])
def login_api():
    data = request.json
    token = login(data.get('username'), data.get('password'))

    if not token:
        return jsonify(message="Invalid credentials"), 401

    response = jsonify(access_token=token)
    set_access_cookies(response, token)
    return response


@auth_views.route('/api/signup', methods=['POST'])
def signup_api():
    data = request.json
    created = create_user(data['username'], data['password'], data['role'])

    if not created:
        return jsonify(message="Signup failed — username exists"), 401

    token = login(data['username'], data['password'])
    response = jsonify(access_token=token)
    set_access_cookies(response, token)
    return response


@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_api():
    return jsonify({
        "message": f"username: {current_user.username}, id: {current_user.id}"
    })


@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged out")
    unset_jwt_cookies(response)
    return response

