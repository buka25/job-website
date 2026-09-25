web: python manage.py seed_media && python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn jobsite.wsgi:application --bind 0.0.0.0:$PORT
