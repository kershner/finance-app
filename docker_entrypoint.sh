#!/bin/sh

# Run Django migrations
python manage.py makemigrations
python manage.py migrate

# Set permissions on newly created DB
chmod 777 /opt/finance_by_month/db.sqlite3

# Start server
(gunicorn app.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"