"""
Подключаем Celery к Django-бэкэнду.
"""

import os
from celery import Celery
from prometheus_client import Counter

# Подключение Django-бэкенда
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
celery_app = Celery("config")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()

# Метрика для отслеживания выполнения задач
task_metric = Counter(
    'celery_task_count', 'Количество выполненных задач Celery', ['name'])
failed_task_metric = Counter(
    'celery_failed_task_count', 'Количество неудачных задач Celery', ['name'])

# Сигнал перед выполнением задачи
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, test.s(), name='add every 10')

# Сигнал перед началом выполнения задачи
@celery_app.task_prerun.connect
def task_prerun_handler(task_id, task, *args, **kwargs):
    task_metric.labels(name=task.name).inc()

# Сигнал после завершения задачи
@celery_app.task_postrun.connect
def task_postrun_handler(task_id, task, *args, **kwargs, state):
    if state == 'error':
        failed_task_metric.labels(name=task.name).inc()
