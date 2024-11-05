"""
Основной проект API SmartIDS.
"""

from .celery import celery_app

__all__ = ('celery_app',)
