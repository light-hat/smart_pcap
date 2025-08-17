"""
Маршруты для пользовательской версии REST API.
"""

# from uuid import uuid4
from django.urls import path

# from django.views.decorators.csrf import csrf_exempt
from ids.views import (
    DumpDetailUpdateDelete,
    DumpListCreate,
    HandledPacketDetailUpdateDelete,
)

urlpatterns = [
    path("dump/", DumpListCreate.as_view()),
    path("dump/<uuid:pk>/", DumpDetailUpdateDelete.as_view()),
    path("dump/<uuid:pk>/packets/", HandledPacketDetailUpdateDelete.as_view()),
]
