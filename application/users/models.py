import json

from application import db, ma
from passlib.hash import pbkdf2_sha256 as sha256

class User(db.Model):
	__tablename__ = 'Users'

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(120), unique = True, nullable = False)
	password = db.Column(db.String(120), nullable = True)
	first_name = db.Column(db.String(120), nullable = True)
	last_name =  db.Column(db.String(120), nullable = True)
	date_of_birth = db.Column(db.DateTime, nullable=True)

	def __init__(self, username, password, first_name, last_name, date_of_birth):
		self.username = username
		self.password = password
		self.first_name = first_name
		self.last_name = last_name
		self.date_of_birth = date_of_birth

	@classmethod
	def find_by_username(cls, username):
   		return cls.query.filter_by(username = username).first()

	@classmethod
	def return_all(cls):
		def to_json(x):
			return {
				'username': x.username,
				'password': x.password
			}
		return {'users': list(map(lambda x: to_json(x), User.query.all()))}

	@staticmethod
	def generate_hash(password):
		return sha256.hash(password)

	@staticmethod
	def verify_hash(password, hash):
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