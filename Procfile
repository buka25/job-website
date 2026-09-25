web: cp -rn media_seed/. media/ 2>/dev/null; python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn jobsite.wsgi:application --bind 0.0.0.0:$PORT
