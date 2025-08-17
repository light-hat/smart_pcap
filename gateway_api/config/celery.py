"""
Подключаем Celery к Django-бэкэнду.
"""

import os

from celery import Celery

# from prometheus_client import Counter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
celery_app = Celery("config")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
