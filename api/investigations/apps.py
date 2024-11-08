"""
Django-приложение для обработки дампов трафика и обработки в Triton.
"""

from django.apps import AppConfig


class InvestigationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "investigations"
