from application import db, ma
from application.users.models import User
from application.reviews.models import Review
from application.attachments.models import Attachment
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import Column, Float, ForeignKey, Integer, LargeBinary, Text
from sqlalchemy.orm import lazyload, relationship

import datetime
import pdb


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
	updated_by_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=True)
	created_by = db.relationship('User', primaryjoin=created_by_id == User.id)
	updated_by = db.relationship('User', primaryjoin=updated_by_id == User.id)
	
	attachments = db.relationship("Attachment", backref="attachments")

	def __repr__(self):
		return '<Item {}>'.format(self.name)

	def __init__(self, name, title, description, price, *args, **kwargs):
		self.name = name
		self.title = title
		self.description = description
		self.price = price
	
	@classmethod
	def create_item(self, newItem, attachments):
		logged_in_user = get_jwt_identity()
		logged_in_user_id = db.session.query(User.id).filter_by(username=logged_in_user).first()
		newItem.created_by_id = logged_in_user_id[0]
		
		if attachments is not None:
			# We have attachments, add 'em
			attachments = Attachment.create_and_add_attachment(attachments)
			if attachments is not None:
				newItem.attachments.append(attachments)
		
		db.session.add(newItem)
		db.session.commit()

	@classmethod
	def update_item(self, item, itemId):
		updated_by = get_jwt_identity()
		logged_in_user = db.session.query(User.id).filter_by(username=updated_by).one()
		
		item.updated_by_id = logged_in_user[0]
		
		existingItem = db.session.query(Item).filter_by(id=itemId).first()
		existingItem.__dict__.update(item.__dict__)
		db.session.add(existingItem)
		db.session.commit()
		return item

	@classmethod
	def get_items(self):
		return db.session.query(Item).options(lazyload('reviews')).order_by(Item.created_date.desc()).all()

	@classmethod
	def get_item_by_id(self, id):
		return db.session.query(Item).options(lazyload('reviews')).get(id)
