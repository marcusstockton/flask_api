import json

from application import db, ma
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import func

class User(db.Model):
	__tablename__ = 'Users'

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(120), unique = True, nullable = False)
	password = db.Column(db.String(120), nullable = True)
	first_name = db.Column(db.String(120), nullable = True)
	last_name =  db.Column(db.String(120), nullable = True)
	date_of_birth = db.Column(db.DateTime, nullable=True)
	avatar = db.Column(db.String(255), nullable = True)
	is_deleted = db.Column(db.Boolean, nullable=False, unique=False, default=False)

	def __init__(self, username, password, first_name, last_name, date_of_birth, avatar, is_deleted):
		self.username = username
		self.password = password
		self.first_name = first_name
		self.last_name = last_name
		self.date_of_birth = date_of_birth
		self.avatar = avatar
		self.is_deleted = is_deleted

	@classmethod
	def get_user_by_id(cls, id):
		''' Returns the user with the specified Id. '''
		return cls.query.get(id)

	@classmethod
	def find_by_username(cls, user):
		''' Returns the user with the specified username. '''
		return cls.query.filter(func.lower(cls.username) == func.lower(user)).first()

	@classmethod
	def return_all(cls):
		''' Returns a list of all users. '''
		def to_json(x):
			return {
				'username': x.username,
				'password': x.password,
				'id': x.id,
				'date_of_birth': x.date_of_birth,
				'first_name': x.first_name,
				'last_name': x.last_name,
				'avatar': x.avatar,
				'is_deleted': x.is_deleted
			}
		
		user_list = cls.query.all()
		return {'users': list(map(lambda x: to_json(x), user_list))}

	@classmethod
	def delete_user(cls, id):
		user = cls.query.filter_by(id = id).first()
		db.session.delete(user)
		db.session.commit()


	@staticmethod
	def generate_hash(password):
		''' Generates a password hash. '''
		return sha256.hash(password)

	@staticmethod
	def verify_hash(password, hash):
		''' Verifies a password and hash. '''
		return sha256.verify(password, hash)

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()


class RevokedTokenModel(db.Model):
	__tablename__ = 'revoked_tokens'
	id = db.Column(db.Integer, primary_key = True)
	jti = db.Column(db.String(120))
	
	def add(self):
		db.session.add(self)
		db.session.commit()
	
	@classmethod
	def is_jti_blacklisted(cls, jti):
		query = cls.query.filter_by(jti = jti).first()
		return bool(query)