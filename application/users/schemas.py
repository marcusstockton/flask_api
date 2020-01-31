from marshmallow import fields, pre_load
from application.users.models import User
from application.attachments.attachment_service import create_attachment_url
from flask import current_app as app, request
from application import ma

class AvatarUrl(fields.Field):
	def _serialize(self, value, attr, obj, **kwargs):
		if value is None:
			return ""	
		return create_attachment_url(value)
		
	def _deserialize(self, value, attr, data, **kwargs):
		return value

class UserSchema(ma.ModelSchema):
	avatar_url = AvatarUrl(attribute="avatar")
	class Meta:
		model = User
		fields=("username", "first_name", "last_name", "date_of_birth", "id", "avatar_url", "is_deleted")
		include_fk=True