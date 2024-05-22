import os
from datetime import timedelta

from celery import Celery

celery_broker_url = os.environ.get('CELERY_BROKER_URL', "redis://localhost:6379/0")

celery_tasks_paths = [
    'data_sources.arxiv',
    'background_processes.create_research',
]

celery_app = Celery(__name__, broker=celery_broker_url, backend=celery_broker_url, include=celery_tasks_paths)
celery_app.conf.broker_connection_retry_on_startup = True

celery_app.conf.beat_schedule = {
    'process_new_articles': {
        'task': 'tasks.tasks.poll_newly_added_articles',
        'schedule': timedelta(minutes=10),
    },
}