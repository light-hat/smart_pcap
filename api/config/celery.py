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

# tasks_counter = Counter('celery_tasks_total', 'Total number of Celery tasks', ['name', 'state'])
#
# @task_prerun.connect
# def task_prerun_handler(task_id, task, *args, **kwargs):
#     tasks_counter.labels(name=task.name, state='started').inc()
#
# @task_success.connect
# def task_success_handler(sender=None, result=None, **kwargs):
#     tasks_counter.labels(name=sender.name, state='succeeded').inc()
#
# @task_failure.connect
# def task_failure_handler(sender=None, task_id=None, exception=None, args=None, **kwargs):
#     tasks_counter.labels(name=sender.name, state='failed').inc()
