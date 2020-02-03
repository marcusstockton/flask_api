from flask import request, render_template, Response, jsonify, make_response
from .models import db, Review
from .schemas import ReviewSchema, ReviewUpdateSchema, ReviewCreateSchema
from sqlalchemy.orm import lazyload, joinedload
from flask import Blueprint, render_template
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from application.reviews.review_service import get_review_by_id, get_reviews_by_item_id, create_review, delete_review_by_id, update_review_by_id

review_profile = Blueprint('review_profile', __name__)


@review_profile.route('/api/reviews/', methods=['GET'])
def get_all_reviews():
    pass

@review_profile.route('/api/items/<int:itemId>/reviews/', methods=['GET'])
def reviews_for_item(itemId):
	review_list = get_reviews_by_item_id(itemId)
	schema = ReviewSchema(many=True)
	return schema.jsonify(review_list)


@review_profile.route("/api/items/<int:itemId>/reviews/<id>", methods=['GET'])
def review_detail(itemId, id):
	item = get_review_by_id(itemId, id)
	schema = ReviewSchema()
	result = schema.dump(item).data
	return (jsonify(result), 200)


@review_profile.route("/api/items/<int:itemId>/reviews/<id>", methods=['PUT'])
@jwt_required
def review_update(itemId, id):
	req_data = request.get_json()
	schema = ReviewUpdateSchema()
	result = schema.load(req_data)
	result = update_review_by_id(itemId, result, get_jwt_identity())
	return (jsonify(result), 200)
	

@review_profile.route("/api/items/<int:itemId>/reviews/create", methods=['POST'])
@jwt_required
def review_create(itemId):
	req_data = request.get_json()
	schema = ReviewCreateSchema()
	data = schema.load(req_data)
	new_review = data.data
	data = create_review(new_review, itemId, get_jwt_identity())
	result = schema.dump(new_review).data
	return (result, 201)


@review_profile.route("/api/items/<int:itemId>/reviews/<int:reviewId>", methods=['DELETE'])
@jwt_required
def delete_review(item_id, review_id):
	delete_review_by_id(item_id, review_id)
	return '', 204