#!/bin/sh
set -e

# Railway's persistent Volume mounts over /app/media owned by root,
# regardless of the wagtail:wagtail ownership baked into the image at
# build time -- this needs root once, here, so the unprivileged
# "wagtail" user below can write there: for the one-off media seed
# step, and for real Wagtail-admin uploads afterwards.
if [ -d /app/media ]; then
    chown -R wagtail:wagtail /app/media
fi

exec su -p -s /bin/sh wagtail -c '
    set -xe
    python manage.py seed_media
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput
    exec gunicorn jobsite.wsgi:application --bind 0.0.0.0:$PORT
'
