#import Requirements
from flask import request
from flask_restful import Resource
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import jwt
from datetime import datetime, timedelta


# Resource for new user registration
class UserRegistration(Resource):
    def post(self):
        try:
            data = request.get_json()
            new_user = User(
                username=data['username'],
                password=generate_password_hash(data['password'], method='sha256'),
                role=data['role']
            )

            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User registered successfully'}, 201
        except Exception as e:
            return {'message': f'Error registering user: {str(e)}'}, 500

# Resource for user login
class UserLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            user = User.query.filter_by(username=data['username']).first()
            if user and check_password_hash(user.password, data['password']):
                login_user(user)
                expiration_time = datetime.utcnow() + timedelta(hours=1)
                token = jwt.encode({'id': str(user.id), 'exp': expiration_time}, 'flaskassigment', algorithm='HS256')

                return {'message': 'Login successful', 'token': token}, 200
            else:
                return {'message': 'Invalid credentials'}, 401
        except Exception as e:
            return {'message': f'Error during login: {str(e)}'}, 500

# Resource for new user logout
class UserLogout(Resource):
    @login_required
    def post(self):
        try:
            logout_user()
            return {'message': 'Logout successful'}, 200
        except Exception as e:
            return {'message': f'Error during logout: {str(e)}'}, 500
