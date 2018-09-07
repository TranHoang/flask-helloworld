web: env PYTHONPATH=$PYTHONPATH:$PWD/app-api gunicorn app-api:app
release: FLASK_APP=manage.py flask db upgrade