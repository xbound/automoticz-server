#!/bin/bash
gunicorn --log-level=debug \
        --workers 4 --name automoticz_api \
        -b 0.0.0.0:8000 \
        --reload automoticz.wsgi:app \
        -t 100000