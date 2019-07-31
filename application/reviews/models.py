import json
import datetime
from sqlalchemy import Column, Float, ForeignKey, Integer, LargeBinary, Text
from sqlalchemy.orm import relationship
from application.users.models import User
from application import db, ma


class Review(db.Model):
	__tablename__ = 'Review'

	id = db.Column(db.Integer, primary_key=True)
	created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
	updated_date = db.Column(db.DateTime, onupdate=datetime.datetime.now())
	rating = db.Column(Integer, nullable=False)
	title = db.Column(Text)
	description = db.Column(Text)

	item_id = db.Column(db.Integer, db.ForeignKey('Items.id'))
	item = relationship('Item', foreign_keys=[item_id], backref="item")

	created_by_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
	updated_by_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

	created_by = db.relationship('User', primaryjoin=created_by_id == User.id, backref="created_by")
	updated_by = db.relationship('User', primaryjoin=updated_by_id == User.id, backref="updated_by")

	def __repr__(self):
		return '<Review {}>'.format(self.Title)

	@classmethod
	def create_review(self):
		db.session.add(self)
		db.session.commit()