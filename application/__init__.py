from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
	"""Construct the core application."""
	app = Flask(__name__, instance_relative_config=False)
	app.config.from_object('config.Config')
	app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
	jwt = JWTManager(app)
	db.init_app(app)
	migrate = Migrate(app, db)
	ma.init_app(app)
	
	# app.config.update(
	# 	TESTING=True,
	# 	SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
	# 	SQLALCHEMY_DATABASE_URI='sqlite:///D:\\Dropbox\\Angular Projects\\AngularShoppingSite\\WebServer\\database.db',
	# 	SQLALCHEMY_TRACK_MODIFICATIONS=False,
	# 	FLASK_APP='wsgi.py'
	# )

	with app.app_context():
		# Imports
		from . import routes

		return app
