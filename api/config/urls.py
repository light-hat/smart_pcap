"""
Конфигурация URL-адресов всего проекта.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [path("admin/", admin.site.urls), path("", include("investigations.urls"))]
