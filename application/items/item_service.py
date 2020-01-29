from application import db
from application.items.models import Item
from sqlalchemy.orm import lazyload, joinedload


def get_items():
    items = db.session.query(Item).options(lazyload('reviews')).order_by(Item.created_date.desc()).all()
    return items

def get_item_by_id(id):
    items = Item.query.options(lazyload('reviews')).filter_by(id=id).first()
    return items