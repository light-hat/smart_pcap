"""
API эндпоинты для дампов.
"""

import logging

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Dump

logger = logging.getLogger(__name__)


class DumpSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=None)
    language = serializers.CharField(max_length=255)


class DumpAPIView(viewsets.ViewSet):
    """
    API для работы с Дампами.
    """

    @extend_schema(
        responses={
            200: OpenApiResponse(description="Список Дампов"),
            400: OpenApiResponse(description="Некорректный запрос"),
            500: OpenApiResponse(description="Внутренняя ошибка сервера"),
        },
        methods=["GET"],
        tags=["dump"],
    )
    def get(self, request):
        """Получение всех объектов."""

        try:
            query = Query(model=Dump)
            result = query.all()

            if result.is_success:
                return Response(result.to_dict(), status=200)
            else:
                return Response(result.to_dict(), status=400)

        except Exception as e:
            logger.error(e)
            return Response(Result(e).to_dict(), status=500)

    @extend_schema(
        request=ProjectSerializer,
        responses={
            201: OpenApiResponse(description="Дамп успешно загружен"),
            400: OpenApiResponse(description="Ошибка валидации данных"),
        },
        methods=["POST"],
        tags=["dump"],
    )
    def post(self, request):
        """Создание нового объекта."""

        try:
            serializer = ProjectSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                command = Command(model=Project, data=data)
                result = command.create()

                if result.is_success:
                    return Response(result.to_dict(), status=201)
                else:
                    return Response(result.to_dict(), status=400)
            return Response(serializer.errors, status=400)

        except Exception as e:
            logger.error(e)
            return Response(Result(e).to_dict(), status=500)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH
            ),
        ],
        request=DumpSerializer,
        responses={
            200: OpenApiResponse(description="Дамп успешно изменён"),
            400: OpenApiResponse(description="Ошибка валидации данных"),
            404: OpenApiResponse(description="Дамп не найден"),
        },
        methods=["PUT"],
        tags=["dump"],
    )
    def put(self, request, pk):
        """Обновление объекта."""

        try:
            serializer = DumpSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                command = Command(
                    model=Dump,
                    entity_id=pk,
                    data=data,
                    foreign_keys={"user": self.request.user.id},
                )
                result = command.update()

                if result.is_success:
                    return Response(result.to_dict(), status=200)
                else:
                    return Response(result.to_dict(), status=400)
            return Response(serializer.errors, status=400)

        except Exception as e:
            logger.error(e)
            return Response(Result(e).to_dict(), status=500)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            204: OpenApiResponse(description="Дамп успешно удалён"),
            404: OpenApiResponse(description="Дамп не найден"),
        },
        methods=["DELETE"],
        tags=["dump"],
    )
    def delete(self, request, pk):
        """Удаление объекта."""

        try:
            command = Command(model=Dump, entity_id=pk)
            result = command.delete()

            if result.is_success:
                return Response(result.to_dict(), status=204)
            else:
                return Response(result.to_dict(), status=400)

        except Exception as e:
            logger.error(e)
            return Response(Result(e).to_dict(), status=500)
