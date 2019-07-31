from application import db, ma
from application.users.models import User
from application.reviews.models import Review
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from sqlalchemy import Column, Float, ForeignKey, Integer, LargeBinary, Text

import datetime
import json




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
		self.created_by = get_jwt_identity()
		db.session.add(self)
		db.session.commit()

	@classmethod
	def update_item(self):
		self.updated_by = get_jwt_identity()
		db.session.add(self)
		db.session.commit()