from flask import request, jsonify
from .models import db, Item
from .schemas import ItemSchema, ItemCreateSchema, ItemUpdateSchema
from sqlalchemy.orm import lazyload
from flask import Blueprint
from flask_jwt_extended import jwt_required


itemprofile = Blueprint('itemprofile', __name__)

@itemprofile.route('/api/items', methods=['GET'])
def items():
	items = Item.get_items()
	schema = ItemSchema(many=True)
	return schema.jsonify(items)


@itemprofile.route("/api/items/<id>", methods=['GET'])
def item_detail(id):
	item = Item.get_item_by_id(id)
	schema = ItemSchema()
	result = schema.dump(item).data
	return jsonify(result)


@itemprofile.route("/api/items/<id>", methods=['PUT'])
@jwt_required
def item_update(id):
	req_data = request.get_json()
	schema = ItemUpdateSchema()
	result = schema.load(req_data)
	Item.update_item(result, id)
	return ('', 204)
		

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
	
