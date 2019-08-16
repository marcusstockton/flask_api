from application import db, ma
from application.users.models import User
from application.reviews.models import Review
from flask_jwt_extended import (get_jwt_identity)
from sqlalchemy import Column, Float, ForeignKey, Integer, LargeBinary, Text
from sqlalchemy.orm import lazyload

import datetime


class Item(db.Model):
	__tablename__ = 'Items'

	id = db.Column(db.Integer, primary_key=True)
	created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
	updated_date = db.Column(db.DateTime, onupdate=datetime.datetime.now())
	name = db.Column(Text)
	title = db.Column(Text)
	description = db.Column(Text)
	price = db.Column(Float, nullable=False)
	reviews = db.relationship(
		'Review',
		backref='review',
		cascade='all, delete, delete-orphan',
		single_parent=True,
		order_by='desc(Review.created_date)'
	)
	created_by_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
	updated_by_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
	created_by = db.relationship('User', primaryjoin=created_by_id == User.id)
	updated_by = db.relationship('User', primaryjoin=updated_by_id == User.id)

	def __repr__(self):
		return '<Item {}>'.format(self.name)
	
	@classmethod
	def create_item(self):
		logged_in_user = db.session.query(User).filter_by(username=updated_by).first()
		self.created_by_id = logged_in_user.id
		db.session.add(self)
		db.session.commit()

	@classmethod
	def update_item(self, item, itemId):
		breakpoint()
		updated_by = get_jwt_identity()
		logged_in_user = db.session.query(User).filter_by(username=updated_by).first()
		item.data["updated_by_id"] = logged_in_user.id
		db.session.query(Item).filter_by(id=itemId).update(item.data)
		db.session.commit()

	@classmethod
	def get_items(self):
		return db.session.query(Item).options(lazyload('reviews')).order_by(Item.created_date.desc()).all()

	@classmethod
	def get_item_by_id(self, id):
		return db.session.query(Item).options(lazyload('reviews')).get(id)