from rest_framework import serializers
from ids.models import Dump


class DumpCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания дампа.
    """
    class Meta:
        model = Dump
        fields = ('id', 'name', 'details', 'source')
        read_only_fields = ('state', )


class DumpUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления информации о дампе.
    """

    class Meta:
        model = Dump
        fields = ('id', 'name', 'details')
        read_only_fields = ('state', )
