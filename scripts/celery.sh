#!/bin/bash
# Run celery worker
celery -A automoticz.celery.celery_app worker -P gevent --loglevel=debug