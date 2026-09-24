web: echo "STEP_1_BEFORE_MIGRATE" && python manage.py migrate --noinput && echo "STEP_2_AFTER_MIGRATE" && gunicorn jobsite.wsgi:application --bind 0.0.0.0:$PORT --log-level debug
