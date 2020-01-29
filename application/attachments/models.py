import os
from application import db, ma
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import Column, Float, ForeignKey, Integer, LargeBinary, Text
from sqlalchemy.orm import lazyload, relationship
from werkzeug.utils import secure_filename
import datetime
from flask import current_app as app

class Attachment(db.Model):
	__tablename__ = 'Attachments'

	id = db.Column(db.Integer, primary_key=True)
	created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
	updated_date = db.Column(db.DateTime, onupdate=datetime.datetime.now())
	created_by_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
	updated_by_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=True)
	item_id = db.Column(db.Integer, db.ForeignKey('Items.id'))
	file_name = db.Column(Text)
	file_extension = db.Column(Text)
	file_path = db.Column(Text, nullable=True)

	def __repr__(self):
		return '<Attachment {}>'.format(self.file_name)

	def __init__(self, file_name, file_extension, *args, **kwargs):
		self.file_name = file_name
		self.file_extension = file_extension
