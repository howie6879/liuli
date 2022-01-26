#!/bin/sh
PIPENV_DOTENV_LOCATION=./.env pipenv run  gunicorn -c src/config/gunicorn.py src.api.http_app:app