"""
Маршруты для пользовательской версии REST API.
"""

from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from .views import DumpAPIView

urlpatterns = [
    path("dump/list/", csrf_exempt(DumpAPIView.as_view({"get": "get"}))),
    path("dump/upload/", csrf_exempt(DumpAPIView.as_view({"post": "post"}))),
    path(
        "dump/<int:pk>/status/", csrf_exempt(DumpAPIView.as_view({"get": "status"})),
    ),
    path(
        "dump/<int:pk>/packets/", csrf_exempt(DumpAPIView.as_view({"get": "retrieve"})),
    ),
    path(
        "dump/<int:pk>/", csrf_exempt(DumpAPIView.as_view({"put": "put", "delete": "delete"})),
    ),
]
