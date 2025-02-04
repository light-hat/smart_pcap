"""
Сериализаторы для моделей БД.
"""

from rest_framework import serializers
from ids.models import Dump, HandledPacket


class DumpCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания дампа.
    """

    class Meta:
        """Метаданные сериализатора."""
        model = Dump
        fields = ("id", "name", "details", "source")
        read_only_fields = ("state",)


class DumpUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления информации о дампе.
    """

    class Meta:
        """Метаданные сериализатора."""
        model = Dump
        fields = ("id", "name", "details")
        read_only_fields = ("state",)


class HandledPacketSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения обработанных пакетов.
    """

    class Meta:
        """Метаданные сериализатора."""
        model = HandledPacket
        fields = (
            "id",
            "dump",
            "label",
            "timestamp",
            "source_ip",
            "destination_ip",
            "source_port",
            "destination_port",
            "ip_length",
            "ip_ttl",
            "ip_tos",
            "tcp_data_offset",
            "tcp_flags",
        )
