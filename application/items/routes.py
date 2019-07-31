from flask import request, render_template, Response, jsonify, make_response
from .models import db, Item
from .schemas import ItemSchema
from sqlalchemy.orm import lazyload, joinedload
from flask import Blueprint, render_template
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


itemprofile = Blueprint('itemprofile', __name__)

@itemprofile.route('/api/items', methods=['GET'])
def items():
	items = db.session.query(Item).options(lazyload('reviews')).order_by(Item.created_date.desc()).all()
	schema = ItemSchema(many=True)
	results = schema.dumps(items).data
	return schema.jsonify(items)


@itemprofile.route("/api/items/<id>", methods=['GET'])
def item_detail(id):
	item = db.session.query(Item).options(lazyload('reviews')).get(id)
	schema = ItemSchema()
	result = schema.dump(item).data
	return jsonify(result)


@itemprofile.route("/api/items/<id>", methods=['PUT'])
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
		
	

@itemprofile.route("/api/items/create", methods=['POST'])
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
	
