from flask import request, jsonify
from .models import db, Item
from .schemas import ItemSchema, ItemCreateSchema, ItemUpdateSchema
from .item_service import get_item_by_id, get_items, delete_item_by_id, create_new_item, update_item
from sqlalchemy.orm import lazyload
from flask import Blueprint, Response, abort
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
import json
from flask_jwt_extended import get_jwt_identity

item_profile = Blueprint('item_profile', __name__)

@item_profile.route('/api/items', methods=['GET'])
def items():
	items = get_items()
	schema = ItemSchema(many=True)
	#import pdb; pdb.set_trace()
	return schema.jsonify(items), 200


@item_profile.route("/api/items/<int:id>", methods=['GET'])
def item_detail(id):
	item = get_item_by_id(id)
	if item is None:
		return ("", 404)
	else:
		schema = ItemSchema()
		return schema.jsonify(item), 200


@item_profile.route("/api/items/<int:id>", methods=['PUT'])
@jwt_required
def item_update(id):
	upload = None
	schema = ItemSchema()
	raw_data = request.form['data']
	item = json.loads(raw_data)
	if 'file' in request.files:
		upload = request.files['file']
		
	updated_item = update_item(id, item, upload, get_jwt_identity())
	return schema.jsonify(updated_item)
		

@item_profile.route("/api/items/create", methods=['POST'])
@jwt_required
def item_create():
	upload = None
	schema = ItemCreateSchema()

	raw_data = request.form['data']
	req_data = json.loads(raw_data)
	if 'file' in request.files:
		upload = request.files['file']
	try:
		data = schema.load(req_data)
		item = create_new_item(data, upload, get_jwt_identity())
		return schema.jsonify(item), 200
	except ValidationError as ve:
		print(ve)
	
@item_profile.route("/api/items/<int:id>/delete", methods=['DELETE'])
@jwt_required
def item_delete(id):
	delete_item_by_id(int(id))
	return ("", 204)
