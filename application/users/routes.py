
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from .models import User, RevokedTokenModel
from flask_restful import Resource, reqparse
from datetime import datetime, timedelta
from flask import Blueprint, render_template

user_profile = Blueprint('user_profile', __name__)


parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)
parser.add_argument('first_name', type=str, required=False)
parser.add_argument('last_name', type=str, required=False)
parser.add_argument('date_of_birth', type = str, required = False)


@user_profile.route("/api/users/register", methods=['POST'])
def user_registration():
	data = parser.parse_args()

	if User.find_by_username(data['username']):
		return {'message': 'User {} already exists'.format(data['username'])}, 303
	
	dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
	
	new_user = User(
            username=data['username'],
            password=User.generate_hash(data['password']),
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=dob
        )
	try:
		new_user.save_to_db()
		access_token = create_access_token(identity=data['username'])
		refresh_token = create_refresh_token(identity=data['username'])
		return {
                    'message': 'User {} was created'.format(data['username']),
                 			'access_token': access_token,
                 			'refresh_token': refresh_token
                }
	except:
		return {'message': 'Something went wrong'}, 500


@user_profile.route("/api/users/login", methods=['POST'])
def user_login():
	data = parser.parse_args()
	current_user = User.find_by_username(data['username'])
	if not current_user:
		return {'message': 'User {} doesn\'t exist'.format(data['username'])}, 404

	if User.verify_hash(data['password'], current_user.password):
		expires = timedelta(days=7)
		access_token = create_access_token(
			identity=data['username'], expires_delta=expires)
		refresh_token = create_refresh_token(identity=data['username'])
		return {
                    'user': current_user.username,
                 			'access_token': access_token,
                 			'refresh_token': refresh_token
                }
	else:
		return {'message': 'Wrong credentials'}


@user_profile.route("/api/users/logout", methods=['POST'])
@jwt_required
def user_logout_access():
	jti = get_raw_jwt()['jti']
	try:
		revoked_token = RevokedTokenModel(jti=jti)
		revoked_token.add()
		return {'message': 'Access token has been revoked'}
	except:
		return {'message': 'Something went wrong'}, 500


@user_profile.route("/api/users/logout_refresh", methods=['POST'])
@jwt_refresh_token_required
def user_logout_refresh():
	jti = get_raw_jwt()['jti']
	try:
		revoked_token = RevokedTokenModel(jti=jti)
		revoked_token.add()
		return {'message': 'Refresh token has been revoked'}
	except:
		return {'message': 'Something went wrong'}, 500


@user_profile.route("/api/users/token_refresh", methods=['POST'])
@jwt_refresh_token_required
def token_refresh():
	current_user = get_jwt_identity()
	access_token = create_access_token(identity=current_user)
	return {'access_token': access_token}


@user_profile.route("/api/users/all_users", methods=['GET'])
def all_users():
	return User.return_all()


@user_profile.route("/api/users/secret", methods=['GET'])
@jwt_required
def SecretResource():
	return {
		'answer': 42
	}
