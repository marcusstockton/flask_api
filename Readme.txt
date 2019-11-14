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