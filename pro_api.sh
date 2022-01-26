#!/bin/sh
PIPENV_DOTENV_LOCATION=./pro.env pipenv run  gunicorn -c src/config/gunicorn.py src.api.http_app:app