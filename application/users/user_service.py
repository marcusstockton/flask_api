from application import db
from application.users.models import User
from sqlalchemy import func

def get_user_by_id(data):
	return User.query.get(data['id'])

def find_by_username(user_name):
	return User.query.filter(func.lower(User.username) == func.lower(user_name)).first()

def get_all_users():
	return User.query.all()

def delete_user(data):
	user = User.query.filter_by(id=data['id']).first()
	db.session.delete(user)
	db.session.commit()

def create_new_user(data):
	user = User.query.filter_by(email=data['email']).first()
	dob = datetime.strptime(data['date_of_birth'], '%d-%m-%Y')
	if not user:
		new_user = User(
			username=data['username'],
			password=User.generate_hash(data['password']),
			first_name=data['first_name'],
			last_name=data['last_name'],
			date_of_birth=dob,
			avatar=avatar.file_name,
			is_deleted=False
		)
		return new_user
	else:
		# User already exists, just return it.
		return user

def save_changes(data):
	db.session.add(data)
	db.session.commit()