"""
Django-приложение для обработки дампов трафика и обработки в Triton.
"""

from django.apps import AppConfig


class InvestigationsConfig(AppConfig):
    """
    Конфигурация Django-приложения для обработки дампов трафика.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "investigations"
