from marshmallow import fields, pre_load
from application.users.models import User
from application import ma

class UserSchema(ma.ModelSchema):
	class Meta:
		model = User
		fields=("username", "first_name", "last_name", "date_of_birth", "id")
		include_fk=True