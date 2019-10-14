from marshmallow import fields, pre_load, post_load
from application.attachments.models import Attachment
from application import ma

class AttachmentSchema(ma.ModelSchema):
	created_by = fields.Nested("UserSchema", many=False, only=["username", 'first_name', 'last_name', 'date_of_birth'], kwargs='created_by_id')
	updated_by = fields.Nested("UserSchema", many=False, only=["username", 'first_name', 'last_name', 'date_of_birth'], kwargs='updated_by_id')
	item = fields.Nested("ItemSchema", many=False, kwargs='item_id')

	class Meta:	
		model = Attachment
		fields = ("id", 'created_date', 'updated_date', 'created_by_id', 'updated_by_id', 'created_by', 'file_name', 'file_extension', 'item_id', 'updated_by', 'item')
		include_fk = True

	@post_load
	def make_object(self, data):
		return Attachment(**data)