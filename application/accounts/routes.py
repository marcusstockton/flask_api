from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from application.users.models import User
from application.users.schemas import UserSchema
from application.users.user_service import find_by_username

account_profile = Blueprint('accountProfile', __name__)

@account_profile.route("/api/account", methods=['GET'])
@jwt_required
def get():
	account_name = get_jwt_identity()
	if account_name is None:
		return ("Unable to find logged in user", 404)
	account = find_by_username(account_name)
	#import pdb; pdb.set_trace()
	schema = UserSchema()
	return schema.jsonify(account)
	
