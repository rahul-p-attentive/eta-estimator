.PHONY: makemigrations migrate runserver

makemigrations:
	poetry run python manage.py makemigrations

migrate: makemigrations
	poetry run python manage.py migrate

runserver:
	poetry run python manage.py runserver

createsuperuser:
	poetry run python manage.py createsuperuser

create_trades:
	python create_trades.py

create_estimators:
	python create_estimators.py