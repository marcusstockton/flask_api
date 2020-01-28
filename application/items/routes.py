from flask import request, jsonify
from .models import db, Item
from .schemas import ItemSchema, ItemCreateSchema, ItemUpdateSchema
from .item_service import get_item_by_id, get_items
from sqlalchemy.orm import lazyload
from flask import Blueprint, Response, abort
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
import json

item_profile = Blueprint('item_profile', __name__)

@item_profile.route('/api/items', methods=['GET'])
def items():
	items = get_items()
	schema = ItemSchema(many=True)
	return schema.jsonify(items)


@item_profile.route("/api/items/<int:id>", methods=['GET'])
def item_detail(id):
	item = get_item_by_id(id)
	if item is None:
		return ("", 404)
	else:
		schema = ItemSchema()
		result = schema.dump(item)
		return (jsonify(result), 200)


@item_profile.route("/api/items/<int:id>", methods=['PUT'])
@jwt_required
def item_update(id):
	upload = None
	if 'file' in request.files:
		raw_data = request.form['data']
		req_data = json.loads(raw_data)
		upload = request.files['file']
	else:
		raw_data = request.form['data']
		req_data = json.loads(raw_data)
	schema = ItemSchema()
	try:
		result = schema.from_dict(req_data)
		item = Item.update_item(result, id, upload)
		return schema.jsonify(item)
	except ValidationError as ve:
		response = jsonify(message=ve.messages)
		#import pdb; pdb.set_trace()
		# return (response, 500)
		# return (json.dumps({ "error": ve.messages }), 500)
		# return Response(ve, status=500,)
		abort(ve, description=ve.messages)
		

@item_profile.route("/api/items/create", methods=['POST'])
@jwt_required
def item_create():
	if 'file' in request.files:
		raw_data = request.form['data']
		req_data = json.loads(raw_data)
		upload = request.files['file']
	else:
		req_data = request.get_json()
	
	schema = ItemCreateSchema()
	try:
		data = schema.load(req_data)
		Item.create_item(data, upload)
		result = schema.dump(data)

		return (result, 201)
	except ValidationError as ve:
		print(ve)
	
@item_profile.route("/api/items/<int:id>/delete", methods=['DELETE'])
@jwt_required
def item_delete(id):
	Item.delete_item_by_id(int(id))
	return ("", 204)
