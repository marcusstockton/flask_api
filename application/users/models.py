from application import db, ma

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