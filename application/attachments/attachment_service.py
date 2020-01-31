from flask import current_app as app, request
from werkzeug.utils import secure_filename
from application.attachments.models import Attachment
import os
import datetime


def create_and_add_attachment(file, userid):
	# See https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
	file_upload_directory = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
	filename = secure_filename(file.filename)

	new_item = Attachment(
		file_name = filename,
		created_date=datetime.datetime.now,
		created_by_id = userid,
		file_extension = os.path.splitext(filename)[1],
		file_path = os.path.join(file_upload_directory, filename)
	)
	if not os.path.exists(file_upload_directory):
		os.mkdir(file_upload_directory)
		
	file.save(os.path.join(file_upload_directory, filename))
	return new_item


def create_attachment_url(filename):
	return '/'.join([request.url_root[:-1], app.config['UPLOAD_FOLDER'], filename])