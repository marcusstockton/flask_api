from application import db, ma
from sqlalchemy import Column, Float, ForeignKey, Integer, LargeBinary, Text
from application.users.models import User
from flask_jwt_extended import get_jwt_identity, get_current_user, get_raw_jwt
import datetime


class Address(db.Model):
    __tablename__ = 'Address'

    id = db.Column(db.Integer, primary_key=True)
    # Audit info
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    updated_date = db.Column(db.DateTime, onupdate=datetime.datetime.now())
    created_by_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    updated_by_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=True)
    created_by = db.relationship('User', primaryjoin=created_by_id == User.id)
    updated_by = db.relationship('User', primaryjoin=updated_by_id == User.id)

    address_line_1 = db.Column(Text, nullable=False)
    address_line_2 = db.Column(Text)
    address_line_3 = db.Column(Text)
    postcode = db.Column(Text, nullable=False)
    city = db.Column(Text)
    county = db.Column(Text)
    main_phone_number = db.Column(Text)

    def __repr__(self):
        return '<Address {}>'.format(self.address_line_1)

    def __init__(self, address_line_1, address_line_2, address_line_3, postcode, city, county, main_phone_number, *args, **kwargs):
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.address_line_3 = address_line_3
        self.postcode = postcode
        self.city = city
        self.county = county
        self.main_phone_number = main_phone_number


    @classmethod
    def create_address(self, address):
        ''' Creates an address '''
        logged_in_user = get_jwt_identity()
        current_user = get_current_user()
        raw_jwt = get_raw_jwt()
        breakpoint()
        logged_in_user_id = db.session.query(User.id).filter_by(username=logged_in_user).first()
        
        address.created_by_id = logged_in_user_id[0]
        db.session.add(address)
        db.session.commit()

    @classmethod
    def get_all(self):
        ''' Returns all addresses, ordered by created date desc '''
        return db.session.query(Address).order_by(Address.created_date.desc()).all()

    @classmethod
    def get_by_id(self, id):
        ''' Returns the address with the specified id. '''
        return db.session.query(Address).get(id)