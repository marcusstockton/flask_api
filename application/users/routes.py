
from flask_jwt_extended import (create_access_token, create_refresh_token,
								jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from application.users.user_service import get_all_users, find_by_username, create_new_user, delete_user, verify_hash
from application.attachments.attachment_service import create_and_add_attachment
from application.users.schemas import UserSchema
from flask_restful import Resource
from datetime import datetime, timedelta
from flask import Blueprint, request
import json

user_profile = Blueprint('user_profile', __name__)


@user_profile.route("/api/users/register", methods=['POST'])
def user_registration():
	upload = None
	if 'avatar' in request.files:
		upload = request.files['avatar']
	
	raw_data = request.form['data']
	req_data = json.loads(raw_data)
	user = find_by_username(req_data['username'])
	if user:
		return {'message': 'User {} already exists'.format(req_data['username'])}, 303
	
	if upload:
		avatar = create_and_add_attachment(upload, user)
	
	req_data['avatar'] = avatar.file_path
	
	try:
		user = create_new_user(req_data)
		
		access_token = create_access_token(identity=req_data['username'])
		refresh_token = create_refresh_token(identity=req_data['username'])
		return {
					'message': 'User {} was created'.format(req_data['username']),
				 			'access_token': access_token,
				 			'refresh_token': refresh_token
				}
	except:
		return {'message': 'Something went wrong'}, 500


@user_profile.route("/api/users/login", methods=['POST'])
def user_login():
	data = json.loads(request.data)
	current_user = find_by_username(data['username'])
	if not current_user:
		return {'message': 'User {} doesn\'t exist'.format(data['username'])}, 404
	
	if verify_hash(data['password'], current_user.password):
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
	users = get_all_users()
	schema = UserSchema(many=True)
	return schema.jsonify(users)


@user_profile.route("/api/users/secret", methods=['GET'])
@jwt_required
def SecretResource():
	return {
		'answer': 42
	}

@user_profile.route("/api/users/<int:id>/delete", methods=['DELETE'])
def delete_user(id):
	try:
		delete_user(id)
		return {'message': 'User Deleted sucessfully.'}, 204
	except Exception as e:
		return e, 500