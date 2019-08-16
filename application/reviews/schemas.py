from marshmallow import fields, pre_load

from application.users.schemas import UserSchema
from application.reviews.models import Review

from application import ma

class ReviewSchema(ma.ModelSchema):
	created_by = fields.Nested(UserSchema, many=False, only=["username", 'first_name', 'last_name', 'date_of_birth'], kwargs='created_by_id')
	updated_by = fields.Nested(UserSchema, many=False, only=["username", 'first_name', 'last_name', 'date_of_birth'], kwargs='updated_by_id')
	class Meta:
		model = Review
		fields=('created_date', 'rating', 'title', 'description','created_by', 'updated_by')
		include_fk = True