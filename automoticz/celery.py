from automoticz.app import init_celery

celery_app = init_celery(celery_context=True)
