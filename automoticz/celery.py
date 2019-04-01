from celery import Celery
from celery.schedules import crontab

from automoticz.app import init_celery


celery_app = init_celery()
