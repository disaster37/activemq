#!/bin/sh

python /app/entrypoint/init/Init.py
exec /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
