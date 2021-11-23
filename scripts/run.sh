#!/bin/bash

if [[ "${FLASK_ENV}" == "development" ]]; then
    flask run --host=0.0.0.0 --port 8050
else
    gunicorn wsgi:app \
        --bind 0.0.0.0:8050 \
        --workers 2 \
        --threads 2
fi
