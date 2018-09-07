web: env PYTHONPATH=$PYTHONPATH:$PWD/app-api gunicorn app-api:app
release: env FLASK_APP=app-api/manage.py flask db upgrade