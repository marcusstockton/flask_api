from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
	"""Construct the core application."""
	app = Flask(__name__, instance_relative_config=False, static_folder='./uploads')
	CORS(app)
	app.config.from_object('config.Config')
	app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
	jwt = JWTManager(app)
	db.init_app(app)
	migrate = Migrate(app, db)
	ma.init_app(app)
	
	with app.app_context():
		from application.users.routes import user_profile
		from application.items.routes import item_profile
		from application.reviews.routes import review_profile
		from application.addresses.routes import address_profile

		app.register_blueprint(user_profile)
		app.register_blueprint(item_profile)	
		app.register_blueprint(review_profile)
		app.register_blueprint(address_profile)

		migrate.init_app(app, db)

		return app
