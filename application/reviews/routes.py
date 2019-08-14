from flask import request, render_template, Response, jsonify, make_response
from .models import db, Review
from .schemas import ReviewSchema
from sqlalchemy.orm import lazyload, joinedload
from flask import Blueprint, render_template
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

review_profile = Blueprint('review_profile', __name__)


@review_profile.route('/api/reviews/', methods=['GET'])
def get_all_reviews():
    pass

@review_profile.route('/api/reviews/<itemId>', methods=['GET'])
def reviews_for_item(itemId):
    review_list = db.session.query(Review).filter(Review.item_id == itemId)
    schema = ReviewSchema(many=True)
    return schema.jsonify(review_list)

@review_profile.route("/api/reviews/<id>", methods=['GET'])
def review_detail(id):
	# item = db.session.query(Item).options(lazyload('reviews')).get(id)
	# schema = ItemSchema()
	# result = schema.dump(item).data
	# return jsonify(result)
    pass

@review_profile.route("/api/reviews/<id>", methods=['PUT'])
@jwt_required
def item_update(id):
	# item = db.session.query(Item).get(id)
	# req_data = request.get_json()
	# schema = ItemSchema()
	# result = schema.load(req_data)
	# Item.update_item(result)
	# try:
	# 	db.session.merge(result.data)
	# 	db.session.commit()
	# 	return schema.dump(result).data
	# except Exception as e:
	# 	breakpoint()
	pass
	

@review_profile.route("/api/items/create", methods=['POST'])
@jwt_required
def item_create():
	# req_data = request.get_json()
	# schema = ItemSchema()
	# result = schema.load(req_data)
	# new_item = result.data
	# Item.create_item(new_item)
	# try:
	# 	db.session.add(new_item)
	# 	db.session.commit()
	# 	return ('', 204)
	# except Exception as e:
	# 	breakpoint()
	pass
