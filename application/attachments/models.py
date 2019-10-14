import os
from application import db, ma
from application.users.models import User
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
	created_by = db.relationship('User', primaryjoin=created_by_id == User.id)
	updated_by = db.relationship('User', primaryjoin=updated_by_id == User.id)

	file_name = db.Column(Text)
	file_extension = db.Column(Text)
	file_path = db.Column(Text)

	# Relationship and fk back to Item
	item = db.relationship('Item', backref="item")
	item_id = db.Column(db.Integer, db.ForeignKey('Items.id'))

	def __repr__(self):
		return '<Attachment {}>'.format(self.file_name)

	def __init__(self, file_name, file_extension, *args, **kwargs):
		self.file_name = file_name
		self.file_extension = file_extension

	
	@classmethod
	def create_and_add_attachment(self, file):
		# See https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
		file_upload_directory = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
		filename = secure_filename(file.filename)
		logged_in_user = get_jwt_identity()
		logged_in_user_id = db.session.query(User.id).filter_by(username=logged_in_user).first()
		new_item = Attachment(
			file_name = filename,
			created_date=datetime.datetime.now,
			created_by_id = logged_in_user_id,
			created_by = logged_in_user,
			file_extension = os.path.splitext(filename)[1],
			file_path = os.path.join(file_upload_directory, filename)
		)
		if not os.path.exists(file_upload_directory):
			os.mkdir(file_upload_directory)
			
		file.save(os.path.join(file_upload_directory, filename))
		return new_item
		

	@classmethod
	def get_attachment(self, id):
		breakpoint()
