"""
API эндпоинты для дампов.
"""

import logging

from ids.serializers import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ids.models import (Dump, Packet)
from ids.serializers import (DumpCreateSerializer, DumpUpdateSerializer)
from rest_framework.parsers import MultiPartParser
from drf_spectacular.utils import extend_schema

logger = logging.getLogger(__name__)


class DumpListCreate(ListCreateAPIView):
    queryset = Dump.objects.all()
    serializer_class = DumpCreateSerializer
    parser_classes = [MultiPartParser]

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'Название',
                    },
                    'details': {
                        'type': 'string',
                        'description': 'Описание',
                    },
                    'source': {
                        'type': 'string',
                        'format': 'binary',
                    },
                },
                'required': ['source'],
            }
        },
        responses={
            201: 'Файл успешно загружен',
            400: 'Ошибка валидации',
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DumpDetailUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Dump.objects.all()
    serializer_class = DumpUpdateSerializer

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return response
