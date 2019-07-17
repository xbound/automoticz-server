#!/bin/bash
# Run uwsgi server
uwsgi --http 0.0.0.0:5000 \
      --gevent 1000 \
      --http-websockets \
      --master \
      --wsgi-file automoticz/wsgi.py \
      --callable server