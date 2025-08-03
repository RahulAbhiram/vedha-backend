web: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py create_admin || true && gunicorn recursion_backend.wsgi:application --bind 0.0.0.0:$PORT
