"""
Маршруты для пользовательской версии REST API.
"""

from uuid import uuid4
from django.urls import path
#from django.views.decorators.csrf import csrf_exempt
from ids.views import (
    DumpListCreate,
    DumpDetailUpdateDelete
)

urlpatterns = [
    path('dump/', DumpListCreate.as_view()),
    path('dump/<uuid:pk>/', DumpDetailUpdateDelete.as_view()),
]
