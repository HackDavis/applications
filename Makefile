all:
	export FLASK_APP=app.py && flask run

install:
	pip3 install -r requirements.txt

format:
	autopep8 --in-place --aggressive --aggressive *.py

deploy:
	pm2 start start.sh

