from application import db
from application.attachments.models import Attachment


def create_and_add_attachment(file, user):
	# See https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
	file_upload_directory = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
	filename = secure_filename(file.filename)

	new_item = Attachment(
		file_name = filename,
		created_date=datetime.datetime.now,
		created_by_id = user.id,
		created_by = user,
		file_extension = os.path.splitext(filename)[1],
		file_path = os.path.join(file_upload_directory, filename)
	)
	if not os.path.exists(file_upload_directory):
		os.mkdir(file_upload_directory)
		
	file.save(os.path.join(file_upload_directory, filename))
	return new_item

