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
from ids.tasks import process_dump_file

logger = logging.getLogger(__name__)


class DumpListCreate(ListCreateAPIView):
    """
    API-обработчики для получения списка и
    создания объектов дампа.
    """
    queryset = Dump.objects.all()
    serializer_class = DumpCreateSerializer
    parser_classes = [MultiPartParser]

    def perform_create(self, serializer):
        """
        Выполняется перед сохранением объекта.
        Запускает Celery-задачу обработки дампа.
        :param serializer: Сериализатор объекта дампа.
        """
        dump = serializer.save()
        process_dump_file.delay(dump.id)

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
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Обработка POST-запроса для дампа.
        :param request: Объект HTTP-запроса.
        :return: Объект HTTP-ответа.
        """
        response = super().post(request, *args, **kwargs)
        return response


class DumpDetailUpdateDelete(RetrieveUpdateDestroyAPIView):
    """
    API-обработчики для детального просмотра,
    изменения и удаления объекта дампа.
    """
    queryset = Dump.objects.all()
    serializer_class = DumpUpdateSerializer
