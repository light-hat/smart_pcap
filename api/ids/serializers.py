from rest_framework import serializers
from ids.models import Dump


class DumpCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания дампа.
    """
    class Meta:
        model = Dump
        fields = ['id', 'name', 'details', 'source']


class DumpUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления информации о дампе.
    """

    class Meta:
        model = Dump
        fields = ['id', 'name', 'details']
