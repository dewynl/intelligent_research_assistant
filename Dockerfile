FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

ENV CELERY_BROKER_URL=redis://redis:6379
ENV FLASK_APP_HOST=0.0.0.0

CMD sh -c 'celery -A celery_setup.celery_app worker --loglevel=info & celery -A celery_setup.celery_app beat & fastapi run main.py'