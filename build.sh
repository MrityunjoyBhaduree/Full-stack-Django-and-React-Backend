#!/bin/bash
# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Make migrations for all apps
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
