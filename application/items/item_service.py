from application import db
from application.items.models import Item
from sqlalchemy.orm import lazyload


def get_items():
    return db.session.query(Item).options(lazyload('reviews')).order_by(Item.created_date.desc()).all()

def get_item_by_id(id):
    return Item.query.filter_by(id=id).first()