# Makefile
## 🌶 flask and hot-reload
flask:
	docker-compose run --rm -e FLASK_APP=secdash.py -e FLASK_ENV=development --service-ports flask-server flask run --host 0.0.0.0 --port 5050

flaskdebug:
	docker-compose run --rm -e DEBUGGER=True -e FLASK_APP=secdash.py -e FLASK_ENV=development --service-ports flask-server flask run --host 0.0.0.0 --port 5050
