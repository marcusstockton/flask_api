from marshmallow import fields, pre_load, post_load

from application.users.schemas import UserSchema
from application.reviews.models import Review

from application import ma

class ReviewSchema(ma.ModelSchema):
	created_by = fields.Nested(UserSchema, many=False, only=["username", 'first_name', 'last_name', 'date_of_birth'], kwargs='created_by_id')
	updated_by = fields.Nested(UserSchema, many=False, only=["username", 'first_name', 'last_name', 'date_of_birth'], kwargs='updated_by_id')
	class Meta:
		model = Review
		fields=('created_date', 'rating', 'title', 'description','created_by', 'updated_by', 'id')
		include_fk = True

	def make_object(self, data):
		return Review(**data)
	
class ReviewUpdateSchema(ma.Schema):
	class Meta:
		fields=("id", 'rating', 'description', 'title')

class ReviewCreateSchema(ma.Schema):

	class Meta:
		fields=('rating', 'description', 'title')

	@post_load
	def make_review(self, data, **kwargs):
		return Review(**data)
