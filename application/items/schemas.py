from marshmallow import fields, pre_load, post_load, EXCLUDE
from application.items.models import Item
from application.users.schemas import UserSchema
from application.reviews.schemas import ReviewSchema
from application.attachments.schemas import AttachmentSchema
from application import ma

class ItemSchema(ma.ModelSchema):
	uppername = fields.Function(lambda obj: obj.name.upper())
	created_by = fields.Nested(UserSchema, many=False, only=["username", 'first_name', 'last_name', 'date_of_birth'], kwargs='created_by_id')
	reviews = fields.Nested(ReviewSchema, many=True, only=["created_date", "rating", "title", "description", "id"])
	updated_by = fields.Nested(UserSchema, many=False, only=["username", 'first_name', 'last_name', 'date_of_birth'], kwargs='updated_by_id')
	attachments = fields.Nested(AttachmentSchema, many=True, only=["created_date", "file_name", "id"])
	_links = ma.Hyperlinks(
		{
			"url": ma.URLFor("itemprofile.item_detail", id="<id>"), 
			"collection": ma.URLFor("itemprofile.items")
		}
	)
	
	class Meta:	
		model = Item
		fields = ("id", 'title', 'description', 'name', 'price', 'reviews', 'uppername', 'created_date', 'created_by_id', 'updated_date', 'created_by', 'updated_by', 'updated_by_id', 'attachments', '_links')
		include_fk = True

	def make_object(self, data):
		return Item(**data)
		
	# @pre_load(pass_many=true)
	# def set_updated(self, data, many):
		# data["updated_date"] = str(datetime.datetime.now())
				

class ItemCreateSchema(ma.Schema):
	attachments = fields.Nested(AttachmentSchema, many=True, only=["created_date", "file_name", "file_extension", "id"])
	created_by = fields.Nested("UserSchema", many=False, only=["username", 'first_name', 'last_name', 'date_of_birth'], kwargs='created_by_id')

	class Meta:	
		model = Item
		fields = ("id", 'title', 'description', 'price', 'name', 'attachments','created_date', 'created_by_id', 'created_by')
	
	@post_load
	def make_object(self, data, **kwargs):
		return Item(**data)
		

class ItemUpdateSchema(ma.Schema):
	attachments = ma.Nested(AttachmentSchema, many=True, only=["created_date", "file_name", "file_extension", "id"])
	
	class Meta:
		model = Item
		unknown = EXCLUDE
		fields = ('id', 'title', 'description', 'name', 'price','attachments','created_date')

	@pre_load
	def make_object(self, data, **kwargs):
		return Item(**data)