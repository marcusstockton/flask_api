export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
export FLASK_ENV=development
export APP_CONFIG_FILE=config.ini
flask run

read -p "Press enter to continue"