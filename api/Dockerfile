FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
    curl

WORKDIR /home/app/web

RUN pip install Django djangorestframework djangorestframework-simplejwt drf-spectacular gunicorn psycopg2-binary Celery redis scapy torch tritonclient[http] numpy transformers django-prometheus prometheus-client

RUN pip install opensearch-py

COPY . .

FROM base AS app

RUN chmod +x entrypoint.sh

RUN python manage.py collectstatic --noinput

ENTRYPOINT ["sh", "./entrypoint.sh"]

FROM base AS worker

RUN python manage.py collectstatic --noinput

CMD ["celery", "-A", "config", "worker", "--loglevel=info"]

FROM base AS flower

RUN pip install flower

CMD ["celery", "-A", "config", "flower", "--port=5555"]
