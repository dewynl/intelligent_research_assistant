import os
from celery import Celery

celery_broker_url = os.environ.get('CELERY_BROKER_URL', "redis://localhost:6379/0")

celery_app = Celery(__name__, broker=celery_broker_url, backend=celery_broker_url, include=['tasks.tasks', 'tasks.nlp'])
celery_app.conf.broker_connection_retry_on_startup = True

print(celery_app)