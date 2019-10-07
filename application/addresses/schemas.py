from application import ma
from marshmallow import fields, pre_load
from application.users.schemas import UserSchema
from .models import Address


class AddressSchema(ma.ModelSchema):
	postcode = fields.Function(lambda obj: obj.postcode.upper())
	created_by = fields.Nested(UserSchema, many=False, only=["username", 'first_name', 'last_name', 'date_of_birth'], kwargs='created_by_id')
	updated_by = fields.Nested(UserSchema, many=False, only=["username", 'first_name', 'last_name', 'date_of_birth'], kwargs='updated_by_id')
	
	_links = ma.Hyperlinks(
		{
			"url": ma.URLFor("addressProfile.addressitem", id="<id>"), 
			"collection": ma.URLFor("addressProfile.addresscollection")
		}
	)
	
	class Meta:	
		model = Address
		fields = ("id", 'address_line_1', 'address_line_2', 'address_line_3', 'postcode', 'city', 'county', 'main_phone_number', 'created_by_id', 'updated_date', 'created_by', 'updated_by', 'updated_by_id', '_links')
		include_fk = True

	def make_object(self, data):
		return Address(**data)