#!/bin/bash
# Run server on gunicorn
gunicorn --log-level=debug \
        --worker-class gevent \
        --workers 1 --name automoticz_api \
        -b 0.0.0.0:$PORT \
        --reload automoticz.wsgi:app \
        -t 100000