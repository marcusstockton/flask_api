from application import db, ma
from application.users.models import User
from application.reviews.models import Review
from application.attachments.models import Attachment
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import Column, Float, ForeignKey, Integer, LargeBinary, Text, update
from sqlalchemy.orm import lazyload, relationship

from datetime import datetime
import pdb


class Item(db.Model):
	__tablename__ = 'Items'

	id = db.Column(db.Integer, primary_key=True)
	created_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
	updated_date = db.Column(db.DateTime, onupdate=datetime.now())
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
	def update_item(self, item, itemId, attachments):
		updated_by = get_jwt_identity()
		logged_in_user = db.session.query(User.id).filter_by(username=updated_by).one()
		row = db.session.query(Item).filter_by(id=itemId).first_or_404()
		row.description = item.description
		row.title = item.title
		row.name = item.name
		row.price = item.price
		row.updated_by_id = logged_in_user[0]
		row.updated_date = datetime.now()

		if attachments is not None:
			# We have attachments, add 'em
			attachments = Attachment.create_and_add_attachment(attachments)
			if attachments is not None:
				row.attachments.append(attachments)

		db.session.merge(row)
		db.session.commit()
		return row

	@classmethod
	def get_items(self):
		''' Returns all items, and reviews, ordered by date created. '''
		return db.session.query(Item).options(lazyload('reviews')).order_by(Item.created_date.desc()).all()

	@classmethod
	def get_item_by_id(self, id):
		''' Returns the item with the specified Id. '''
		return db.session.query(Item).options(lazyload('reviews')).get_or_404(id)

	@classmethod
	def delete_item_by_id(self, id):
		''' Deletes the item with the specified Id. '''
		db.session.query(Item).filter_by(id = id).delete()
		db.session.commit()