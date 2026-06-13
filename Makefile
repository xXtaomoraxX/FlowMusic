# Makefile for FlowMusic project

test:
	@ python manage.py test


serve:
	@ python manage.py runserver


makemigrations:
	@ python manage.py makemigrations


migrate:
	@ python manage.py migrate


statics:
	@ python manage.py collectstatic


shell:
	@ python manage.py shell
