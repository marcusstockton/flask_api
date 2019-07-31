from marshmallow import fields, pre_load
from application.items.models import Item
from application.users.schemas import UserSchema
from application.reviews.schemas import ReviewSchema
from application import ma

class ItemSchema(ma.ModelSchema):
	uppername = fields.Function(lambda obj: obj.name.upper())
	created_by = fields.Nested(UserSchema, many=False, only=["username", 'first_name', 'last_name', 'date_of_birth'], kwargs='created_by_id')
	reviews = fields.Nested(ReviewSchema, many=True, only=["created_date", "rating", "title", "description", "id"])
	updated_by = fields.Nested(UserSchema, many=False, only=["username", 'first_name', 'last_name', 'date_of_birth'], kwargs='updated_by_id')
	
	_links = ma.Hyperlinks(
		{
			"url": ma.URLFor("itemprofile.item_detail", id="<id>"), 
			"collection": ma.URLFor("itemprofile.items")
		}
	)
	
	class Meta:	
		model = Item
		fields = ("id", 'title', 'description', 'price', 'reviews', 'uppername', 'created_date', 'updated_date', 'created_by', 'updated_by', '_links')
		include_fk = True

	def make_object(self, data):
		return Item(**data)
		
	# @pre_load(pass_many=True)
	# def set_updated(self, data, many):
		# data["UpdatedDate"] = str(datetime.datetime.now())
				

class ItemCreateSchema(ma.Schema):
	class Meta:
		fields = ("title", "description", "price", "name")