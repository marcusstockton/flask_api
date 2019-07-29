from sqlalchemy import Column, Float, ForeignKey, Integer, LargeBinary, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect, sql
from sqlalchemy_utils import UUIDType, EmailType
from uuid import UUID
import datetime
import uuid
from marshmallow import fields, pre_load
from marshmallow_sqlalchemy import field_for
from passlib.hash import pbkdf2_sha256 as sha256

import json

from . import db, ma


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
        backref='item',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Review.created_date)'
    )
	# created_by = relationship('User', primaryjoin='Review.CreatedById == User.Id')
	# updated_by = relationship('User', primaryjoin='Review.UpdatedById == User.Id')

	def __repr__(self):
		return '<Item {}>'.format(self.name)


class Review(db.Model):
	__tablename__ = 'Review'

	id = db.Column(db.Integer, primary_key=True)
	created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
	updated_date = db.Column(db.DateTime, onupdate=datetime.datetime.now())
	rating = db.Column(Integer, nullable=False)
	title = db.Column(Text)
	description = db.Column(Text)
	item_id = db.Column(db.Integer, db.ForeignKey('Items.id'))
	#item = relationship('Item', backref="item")
	#item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
	#item = db.relationship('Item', backref=db.backref('reviews', lazy=True))
	# created_by = relationship('User', primaryjoin='Review.CreatedById == User.Id')
	# updated_by = relationship('User', primaryjoin='Review.UpdatedById == User.Id')

	def __repr__(self):
		return '<Review {}>'.format(self.Title)



class User(db.Model):
	__tablename__ = 'Users'

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(120), unique = True, nullable = False)
	password = db.Column(db.String(120), nullable = True)
	first_name = db.Column(db.String(120), nullable = True)
	last_name =  db.Column(db.String(120), nullable = True)
	date_of_birth = db.Column(db.DateTime, nullable=True)

	@classmethod
	def find_by_username(cls, username):
   		return cls.query.filter_by(username = username).first()

	@classmethod
	def return_all(cls):
		def to_json(x):
			return {
				'username': x.username,
				'password': x.password
			}
		return {'users': list(map(lambda x: to_json(x), User.query.all()))}

	@staticmethod
	def generate_hash(password):
		return sha256.hash(password)

	@staticmethod
	def verify_hash(password, hash):
		return sha256.verify(password, hash)

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)


class ReviewSchema(ma.ModelSchema):
	# CreatedBy = fields.Nested(AspNetUserSchema)
	# UpdatedBy = fields.Nested(AspNetUserSchema)
	
	class Meta:
		model = Review
		include_fk = True
	

class ItemSchema(ma.ModelSchema):
	uppername = fields.Function(lambda obj: obj.name.upper())
	# CreatedBy = fields.Nested(AspNetUserSchema)
	# UpdatedBy = fields.Nested(AspNetUserSchema)
	Reviews = fields.Nested(ReviewSchema, many=True, only=["created_date", "rating", "title", "description", "id"])
	# UpdatedBy = field_for(Item, "UpdatedBy", dump_only=True)
	
	_links = ma.Hyperlinks(
		{"url": ma.URLFor("item_detail", id="<id>"), "collection": ma.URLFor("items")}
	)
	
	class Meta:	
		model = Item
		#exclude= ('UpdatedBy', "CreatedBy")
		include_fk = True

	def make_object(self, data):
		return Item(**data)
		
	# @pre_load(pass_many=True)
	# def set_updated(self, data, many):
		# data["UpdatedDate"] = str(datetime.datetime.now())
		# data["UpdatedBy"] = db.session.query(AspNetUser).first()
				

class ItemCreateSchema(ma.Schema):
	class Meta:
		fields = ("title", "description", "price", "name")


