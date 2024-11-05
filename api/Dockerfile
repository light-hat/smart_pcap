FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
    curl

WORKDIR /home/app/web

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

FROM base AS app

RUN chmod +x entrypoint.sh

RUN python manage.py collectstatic --noinput

ENTRYPOINT ["sh", "./entrypoint.sh"]

FROM base AS worker

RUN python manage.py collectstatic --noinput

CMD ["celery", "-A", "config", "worker", "--loglevel=info"]
