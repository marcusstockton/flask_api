from flask import request, render_template, Response, jsonify, make_response
from flask_restful import Resource, reqparse
from datetime import datetime as dt
from flask import current_app as app
from .models import db, Item, Review, ItemSchema, ReviewSchema, UserSchema, ItemCreateSchema, User, RevokedTokenModel
from sqlalchemy.orm import lazyload, joinedload
import json
import uuid
import datetime
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)





# ITEMS

@app.route('/api/items', methods=['GET'])
def items():
	items = db.session.query(Item).options(lazyload('reviews')).order_by(Item.created_date.desc()).all()
	schema = ItemSchema(many=True)
	results = schema.dumps(items).data
	return schema.jsonify(items)


@app.route("/api/items/<id>", methods=['GET'])
def item_detail(id):
	item = db.session.query(Item).options(lazyload('reviews')).get(id)
	schema = ItemSchema()
	result = schema.dump(item).data
	return jsonify(result)


@app.route("/api/items/<id>", methods=['PUT'])
@jwt_required
def item_update(id):
	item = db.session.query(Item).get(id)
	req_data = request.get_json()
	schema = ItemSchema()
	result = schema.load(req_data)
	Item.update_item(result)
	try:
		db.session.merge(result.data)
		db.session.commit()
		return schema.dump(result).data
	except Exception as e:
		breakpoint()
		
	

@app.route("/api/items/create", methods=['POST'])
@jwt_required
def item_create():
	req_data = request.get_json()
	schema = ItemSchema()
	result = schema.load(req_data)
	new_item = result.data
	Item.create_item(new_item)
	try:
		db.session.add(new_item)
		db.session.commit()
		return ('', 204)
	except Exception as e:
		breakpoint()
	



# USERS

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)


@app.route("/api/users/register", methods=['POST'])
def user_registration():
	data = parser.parse_args()

	if User.find_by_username(data['username']):
		return {'message': 'User {} already exists'.format(data['username'])}

	new_user = User(
            username = data['username'],
            password = User.generate_hash(data['password']),
			first_name = data['first_name'],
			last_name =  data['last_name'],
			date_of_birth = data['date_of_birth'],
        )
	try:
		new_user.save_to_db()
		access_token = create_access_token(identity = data['username'])
		refresh_token = create_refresh_token(identity = data['username'])
		return {
			'message': 'User {} was created'.format(data['username']),
			'access_token': access_token,
			'refresh_token': refresh_token
			}
	except:
		return {'message': 'Something went wrong'}, 500


@app.route("/api/users/login", methods=['POST'])
def user_login():
	data = parser.parse_args()
	current_user = User.find_by_username(data['username'])
	if not current_user:
		return {'message': 'User {} doesn\'t exist'.format(data['username'])}
	
	if User.verify_hash(data['password'], current_user.password):
		access_token = create_access_token(identity = data['username'])
		refresh_token = create_refresh_token(identity = data['username'])
		return {
			'message': 'Logged in as {}'.format(current_user.username),
			'access_token': access_token,
			'refresh_token': refresh_token
			}
	else:
		return {'message': 'Wrong credentials'}


@app.route("/api/users/logout", methods=['POST'])
@jwt_required
def user_logout_access():
	jti = get_raw_jwt()['jti']
	try:
		revoked_token = RevokedTokenModel(jti = jti)
		revoked_token.add()
		return {'message': 'Access token has been revoked'}
	except:
		return {'message': 'Something went wrong'}, 500
      


@app.route("/api/users/logout_refresh", methods=['POST'])
@jwt_refresh_token_required
def user_logout_refresh():
	jti = get_raw_jwt()['jti']
	try:
		revoked_token = RevokedTokenModel(jti = jti)
		revoked_token.add()
		return {'message': 'Refresh token has been revoked'}
	except:
		return {'message': 'Something went wrong'}, 500
    

@app.route("/api/users/token_refresh", methods=['POST'])
@jwt_refresh_token_required	
def token_refresh():
	current_user = get_jwt_identity()
	access_token = create_access_token(identity = current_user)
	return {'access_token': access_token}


@app.route("/api/users/all_users", methods=['GET'])	
def all_users():
	return User.return_all()
    


@app.route("/api/users/secret", methods=['GET'])
@jwt_required
def SecretResource():
	return {
		'answer': 42
	}
      