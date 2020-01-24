Using the following as reference: 
https://hackersandslackers.com/creating-your-first-flask-application/

Flask-Migrations: https://flask-migrate.readthedocs.io/en/latest/


useful Commands:
To create a migration:  flask db migrate
To update the db: flask db upgrade


To run the site:
cd to the root:
python -m flask run


to generate classes from db:

(Python372) D:\Dropbox\Angular Projects\flask-webserver> 
sqlacodegen sqlite:///../AngularShoppingSite/WebServer/database.db --outfile items --tables Items,Review



{
	"username": "marcus",
	"password": "secret"
}



from application import db
from application.users.models import User
import datetime
u = User(username="marcus", password="secret", first_name="Marcus", last_name="Stockton", date_of_birth=datetime.datetime(1991, 7, 19), avatar="", is_deleted=False)
db.session.add(u)
db.session.commit()