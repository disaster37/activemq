#!/bin/sh

python /app/entrypoint/Init.py
exec /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
