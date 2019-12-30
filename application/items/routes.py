from flask import request, jsonify
from .models import db, Item
from .schemas import ItemSchema, ItemCreateSchema, ItemUpdateSchema
from sqlalchemy.orm import lazyload
from flask import Blueprint, Response, abort
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
import json

itemprofile = Blueprint('itemprofile', __name__)

@itemprofile.route('/api/items', methods=['GET'])
def items():
	items = Item.get_items()
	schema = ItemSchema(many=True)
	return schema.jsonify(items)


@itemprofile.route("/api/items/<int:id>", methods=['GET'])
def item_detail(id):
	item = Item.get_item_by_id(id)
	if item is None:
		return ("", 404)
	else:
		schema = ItemSchema()
		result = schema.dump(item)
		return (jsonify(result), 200)


@itemprofile.route("/api/items/<int:id>", methods=['PUT'])
@jwt_required
def item_update(id):
	if 'file' in request.files:
		raw_data = request.form['data']
		req_data = json.loads(raw_data)
	else:
		req_data = request.form['data']
	schema = ItemSchema()
	try:
		js = json.loads(req_data)
		result = schema.from_dict(js)
		item = Item.update_item(result, id)
		return schema.jsonify(item)
	except ValidationError as ve:
		response = jsonify(message=ve.messages)
		import pdb; pdb.set_trace()
		# return (response, 500)
		# return (json.dumps({ "error": ve.messages }), 500)
		# return Response(ve, status=500,)
		abort(ve, description=ve.messages)
		

@itemprofile.route("/api/items/create", methods=['POST'])
@jwt_required
def item_create():
	if 'file' in request.files:
		raw_data = request.form['data']
		req_data = json.loads(raw_data)
	else:
		req_data = request.get_json()
	
	schema = ItemCreateSchema()
	try:
		data = schema.load(req_data)
		Item.create_item(data, request.files['file'])
		result = schema.dump(data)

		return (result, 201)
	except ValidationError as ve:
		print(ve)
	
@itemprofile.route("/api/items/<int:id>/delete", methods=['DELETE'])
@jwt_required
def item_delete(id):
	Item.delete_item_by_id(int(id))
	return ("", 204)
