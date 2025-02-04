"""
Конфигурация Django-приложения.
"""

from django.apps import AppConfig


class IdsConfig(AppConfig):
    """
    Главное приложение для API.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "ids"
