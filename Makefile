migrate:
	python manage.py makemigrations
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --no-input

runserver:
	python manage.py runserver

all: migrate collectstatic runserver