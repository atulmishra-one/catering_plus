#!/usr/bin/env bash


export DJANGO_SETTINGS_MODULE=app.settings.$CATER_ENV

python manage.py makemigrations account && python manage.py migrate account
python manage.py makemigrations meal && python manage.py migrate meal
python manage.py makemigrations cart && python manage.py migrate cart
python manage.py makemigrations order && python manage.py migrate order
python manage.py raw_material order && python manage.py migrate raw_material
python manage.py makemigrations && python manage.py migrate

