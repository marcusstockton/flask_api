from application import db
from application.items.models import Item
from application.attachments.attachment_service import create_and_add_attachment
from application.users.user_service import find_by_username
from sqlalchemy.orm import lazyload, joinedload
import datetime

def get_items():
	''' Returns a list of all items ordered in created_date descending order '''
	items = db.session.query(Item).options(lazyload('reviews'), lazyload('attachments')).order_by(Item.created_date.desc()).all()
	#import pdb; pdb.set_trace()
	return items


def get_item_by_id(id):
	''' Returns the Item with the specified Id '''
	return Item.query.options(lazyload('reviews'), lazyload('attachments')).filter_by(id=id).first()


def delete_item_by_id(id):
	''' Deletes the item with the specified Id. '''
	db.session.query(Item).filter_by(id = id).delete()
	db.session.commit()


def create_new_item(data, file, userId):
	''' Creates a new Item '''
	if file:
		data.attachments.append(create_and_add_attachment(file, userId))
	save_changes(data)
	return data


def update_item(itemId, item, attachment, userId):
	row = db.session.query(Item).filter_by(id=itemId).first()
	if row:
		row.description = item['description']
		row.title = item['title']
		row.name = item['name']
		row.price = item['price']
		row.updated_by_id = find_by_username(userId).id
		row.updated_date = datetime.datetime.now()

		if attachment:
			# We have attachments, add 'em
			attachments = create_and_add_attachment(attachment, userId)
			if attachments is not None:
				row.attachments.append(attachments)
		db.session.merge(row)
		db.session.commit()
		return row
	else:
		return None

	

def save_changes(data):
	db.session.add(data)
	db.session.commit()