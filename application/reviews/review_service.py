from application import db
from application.reviews.models import Review
from sqlalchemy.orm import lazyload, joinedload
import datetime


def get_review_by_id(item_id, review_id):
	''' Returns the review with the specified Id. '''
	return db.session.query(Review).filter(Review.item_id == item_id).filter(Review.id == review_id).first()


def get_reviews_by_item_id(item_id):
	''' Returns all reviews for the selected item id. '''
	return db.session.query(Review).filter(Review.item_id == item_id)


def create_review(data, item_id, user_id):
	''' Create a new review '''
	data.created_by_id = user_id
	data.item_id = item_id
	save_changes(data)
	return data


def delete_review_by_id(item_id, review_id):
	''' Deletes the review by item_id and review_id '''
	db.session.query(Review).filter_by(item_id = item_id).filter(id = id).delete()
	db.session.commit()


def update_review_by_id( item_id, review, user_id):
	''' Updates the review '''
	review.data["updated_by_id"] = user_id
	db.session.query(Review).filter_by(id=review.data.id).update(review.data)
	db.session.commit()


def save_changes(data):
	db.session.add(data)
	db.session.commit()