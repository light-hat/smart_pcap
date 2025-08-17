FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
    curl

WORKDIR /home/app/web

RUN pip install Django djangorestframework djangorestframework-simplejwt drf-spectacular gunicorn psycopg2-binary scapy opensearch-py confluent-kafka

COPY . .

FROM base AS app

RUN chmod +x entrypoint.sh

RUN python manage.py collectstatic --noinput

ENTRYPOINT ["sh", "./entrypoint.sh"]
