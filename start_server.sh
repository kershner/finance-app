#!/usr/bin/env bash
# start-server.sh

(gunicorn app.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"