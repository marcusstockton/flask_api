import json
import datetime
from sqlalchemy import Column, Float, ForeignKey, Integer, LargeBinary, Text
from sqlalchemy.orm import relationship
from application.users.models import User
from application import db, ma
from flask_jwt_extended import get_jwt_identity


class Review(db.Model):
	__tablename__ = 'Review'

	id = db.Column(db.Integer, primary_key=True)
	created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
	updated_date = db.Column(db.DateTime, onupdate=datetime.datetime.now())
	rating = db.Column(Integer, nullable=False)
	title = db.Column(Text)
	description = db.Column(Text)

	item_id = db.Column(db.Integer, db.ForeignKey('Items.id'))
	created_by_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
	created_by = relationship('User',  foreign_keys='Review.created_by_id')

	updated_by_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
	updated_by = relationship('User',  foreign_keys='Review.updated_by_id')

	def __repr__(self):
		return '<Review {}>'.format(self.__dict__)

	def __init__(self, rating, title, description, *args, **kwargs):
		self.title = title
		self.rating = rating
		self.description = description

	# @classmethod
	# def create_review(self, data):
	# 	logged_in_user = get_jwt_identity()
	# 	logged_in_user_id = db.session.query(
	# 		User.id).filter_by(username=logged_in_user).first()

	# 	data.created_by_id = logged_in_user_id[0]
	# 	breakpoint()
	# 	db.session.add(data)
	# 	db.session.commit()

	# @classmethod
	# def get_reviews_by_item_id(self, item_id):
	# 	''' Returns all reviews for the selected item id. '''
	# 	return db.session.query(Review).filter(Review.item_id == item_id)

	# @classmethod
	# def get_review_by_id(self, item_id, review_id):
	# 	''' Returns the review with the specified Id. '''
	# 	return db.session.query(Review).filter(Review.item_id == item_id).filter(Review.id == review_id).first()

	# @classmethod
	# def update_review_by_id(self, item_id, review):
	# 	''' Updates the review '''
	# 	updated_by = get_jwt_identity()
	# 	logged_in_user = db.session.query(
	# 		User.id).filter_by(username=updated_by).first()
	# 	review.data["updated_by_id"] = logged_in_user[0]
	# 	db.session.query(Review).filter_by(id=review.data.id).update(review.data)
	# 	db.session.commit()

	# @classmethod
	# def delete_review_by_id(self, item_id, review_id):
	# 	''' Deletes the specified review, on the specified item. '''
	# 	db.session.query(Review).filter_by(id = id).delete()
	# 	db.session.commit()
