release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn only_studies.wsgi
